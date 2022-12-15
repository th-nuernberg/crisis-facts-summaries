import os
#import yaml
import json
import argparse
#import dateutil.parser
import streamcorpus
import logging

logging.basicConfig()
logger = logging.getLogger('logger')
#logger.warning('The system may break down')

#try:
# from pathlib import Path
#except ImportError:
#  from pathlib2 import Path  # python 2 backport


#def parse_args():
#    parser = argparse.ArgumentParser()
#    parser.add_argument(
#        '--config-file',
#        dest='config_file',
#        type=str,
#        default='config.yaml'
#    )
#    return parser.parse_args()


#def load_config(file):
#    config = yaml.load(
#        open(file, 'r'), 
#        Loader=yaml.FullLoader
#    )
#    return config


def main():
    #args = parse_args()
    #config = load_config(args.config_file)

    raw_dir = "D:\\Meine Dateien\\Uni\\IT-Projekt\\in"# config['input_dir']
    out_dir ="D:\\Meine Dateien\\Uni\\IT-Projekt\\out"# config['output_dir']
    clean = False

    #Path(out_dir).mkdir(exist_ok=True)
    #os.makedirs(out_dir, exist_ok=True)

    files = [
        file
        for file in os.listdir(raw_dir)
        if 'thrift' in file 
    ]

    for file in files:
        print('process file ' + file)
        docs = []
        name = file.split('.thrift')[0]
        file_in = os.path.join(raw_dir, file)
        file_out = os.path.join(out_dir,  name + '.jsonl')
        for stream_item in streamcorpus.Chunk(file_in):
            # extract relevant content
            print("Noch ok")
            stream_id = stream_item.stream_id
            #stream_time = stream_item.stream_time
            doc_id = stream_item.doc_id
            doc_source = stream_item.source
            meta_data = stream_item.source_metadata
            print("Noch ok 1")
            # prefer cleaned html version
            # with fallback strategy
            used_version = ''
            if clean:
                html = stream_item.body.clean_html
                used_version = 'clean_html'
                if html is None:
                    html = stream_item.body.clean_visible
                    used_version = 'clean_visible'
                if html is None:
                    html = stream_item.body.raw
                    used_version = 'raw'
            else:
                html = stream_item.body.raw
                used_version = 'raw'

            doc = {
                'stream_id': stream_id,
                'document_id': doc_id,
                'document_source': doc_source,
                #'timestamp': stream_time.zulu_timestamp,
                'lang': meta_data.get('lang', 'unknown'),
                'version': used_version,
                'html': html
            }
            docs.append(doc)
            print("Noch ok 2")

        # sort by timestamp
        #docs = sorted(docs, key=lambda doc: dateutil.parser.isoparse(doc['timestamp']))

        # save extracted content
        if os.path.isfile(file_out):
            os.remove(file_out)
            
        with open(file_out, 'a') as f:
            for doc in docs:
                f.write(json.dumps(doc) + '\n')
        print("Done")


#if __name__ == '__main__':
main()