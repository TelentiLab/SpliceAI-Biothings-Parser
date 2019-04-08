import logging
import os
import time
import datetime

FILE_NOT_FOUND_ERROR = 'Cannot find input file: {}'   # error message constant

# configure logger
logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
_logger = logging.getLogger('SpliceAI')

# change following parameters accordingly
SOURCE_NAME = 'splice_ai'   # source name that appears in the api response
FILENAME = 'whole_genome_filtered_spliceai_scores.vcf'   # name of the file to read
DELIMITER = '\t'    # the delimiter that separates each field


def _inspect_file(filename: str) -> int:
    i = 0
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def load_data(data_folder: str):
    """
    Load data from a specified file path. Parse each line into a dictionary according to the schema.
    Then process each dict by normalizing data format, remove null fields (optional).
    Append each dict into final result using its id.

    :param data_folder: the path(folder) where the data file is stored
    :return: a generator that yields data.
    """
    input_file = os.path.join(data_folder, FILENAME)
    # raise an error if file not found
    if not os.path.exists(input_file):
        _logger.error(FILE_NOT_FOUND_ERROR.format(input_file))
        raise FileExistsError(FILE_NOT_FOUND_ERROR.format(input_file))

    file_lines = _inspect_file(input_file)  # get total lines so that we can indicate progress in next step

    with open(input_file, 'r') as file:
        start_time = time.time()
        _logger.info(f'start reading file: {FILENAME}')
        count = 0
        skipped = []
        for line in file:
            count += 1
            ratio = count / file_lines
            time_left = datetime.timedelta(seconds=(time.time() - start_time) * (1 - ratio) / ratio)
            # format to use 2 decimals for progress
            _logger.info(f'reading line {count} ({(count / file_lines * 100):.2f}%), estimated time left: {time_left}')

            if line.startswith('#') or line.strip() == '':
                skipped.append(line)
                continue  # skip commented/empty lines

            try:
                # unpack according to schema
                chrom, pos, _id, ref, alt, qual, _filter, info = line.strip().split(DELIMITER)
            except ValueError:
                _logger.error(f'failed to unpack line {count}: {line}')
                _logger.error(f'got: {line.strip().split(DELIMITER)}')
                skipped.append(line)
                continue  # skip error line

            try:
                """
                Unpack info to retrieve scores.
                Sample info record:
                SYMBOL=TUBB8;STRAND=-;TYPE=E;DIST=-4;DS_AG=0.1391;DS_AL=0.0000;DS_DG=0.0000;DS_DL=0.0000;DP_AG=-1;DP_AL=1;DP_DG=-1;DP_DL=28
                """
                [symbol, strand, _type, distance,
                 ds_ag, ds_al, ds_dg, ds_dl,
                 dp_ag, dp_al, dp_dg, dp_dl] = [each.split('=')[1] for each in info.strip().split(';')]
            except ValueError:
                _logger.error(f'failed to unpack info: {info}')
                _logger.error(f'got: {info.strip().split(";")}')
                skipped.append(line)
                continue  # skip error line

            try:    # parse each field if necessary (format, enforce datatype etc.)
                pos = int(pos)
                pos_strand = strand == '+'
                exonic = _type == 'E'
                distance = int(distance)
                ds_ag = float(ds_ag)
                ds_al = float(ds_al)
                ds_dg = float(ds_dg)
                ds_dl = float(ds_dl)
                dp_ag = int(dp_ag)
                dp_al = int(dp_al)
                dp_dg = int(dp_dg)
                dp_dl = int(dp_dl)
            except ValueError as e:
                _logger.error(f'failed to cast type for line {count}: {e}')
                skipped.append(line)
                continue  # skip error line

            _id = f'chr{chrom}:g.{pos}{ref}>{alt}'  # define id

            variant = {
                'chrom': chrom,
                'pos': pos,
                'ref': ref,
                'alt': alt,
                'scores': [
                    {
                        'hgnc_gene': symbol,
                        'pos_strand': pos_strand,
                        'exonic': exonic,
                        'distance': distance,
                        'acceptor_gain': {
                            'score': ds_ag,
                            'position': dp_ag,
                        },
                        'acceptor_loss': {
                            'score': ds_al,
                            'position': dp_al,
                        },
                        'donor_gain': {
                            'score': ds_dg,
                            'position': dp_dg,
                        },
                        'donor_loss': {
                            'score': ds_dl,
                            'position': dp_dl,
                        },
                    },
                ],
            }

            yield {  # commit an entry by yielding
                "_id": _id,
                SOURCE_NAME: variant
            }
        _logger.info(f'parse completed, {len(skipped)}/{file_lines} lines skipped.')
        for x in skipped:
            _logger.info(f'skipped line: {x.strip()}')
