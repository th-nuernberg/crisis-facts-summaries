import os
import yaml
import json
import argparse
from goose3 import Goose


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config-file',
        dest='config_file',
        type=str,
        required=True
    )
    return parser.parse_args()


def load_config(file):
    config = yaml.load(
        open(file, 'r'), 
        Loader=yaml.FullLoader
    )
    return config


def main():
    #config = load_config(parse_args().config_file)

    input_dir = 'D:\\Meine Dateien\\Uni\\IT-Projekt\\in' #config['preparation']['input_dir']
    out_dir = 'D:\\Meine Dateien\\Uni\\IT-Projekt\\out' #config['preparation']['output_dir']

    os.makedirs(out_dir, exist_ok=True)

    file_paths =['D:\\Meine Dateien\\Uni\\IT-Projekt\\in\\test.jsonl']
    #[
    #    (os.path.join(input_dir, file), file.split('.jsonl')[0])
    #    for file in os.listdir(input_dir)
    #    if '.jsonl' in file
    #]

    for file_path in file_paths:
        # load all documents for file chunk
        print(f'load documents of {file_path}') #{file_path[1]}')
        docs = ['D:\\Meine Dateien\\Uni\\IT-Projekt\\in\\index.html']
        key = file_path#[1]
        #with open (file_path, 'r') as f:#(file_path[0], 'r') as f:
        #    for line in f:
        #        docs.append(json.loads(line))

        # preprocess each document html content
        print(f'process {len(docs)} documents of {key}')
        goose = Goose()
        docs_preprocessed = []
        for doc in docs:
            with open (doc, 'r') as f:
                #print(f.read())
                cont = f.read()
            html = cont #doc#['html']

            article = goose.extract(raw_html=html)
            meta = article.meta_description
            title = article.title
            content = article.cleaned_text
            print(content)

            #clean visible should not contain any html tags
            #if doc['version'] == 'clean_visible':
            content = html

            doc_preprocessed = {
                #'stream_id': doc['stream_id'],
                #'document_id': doc['document_id'],
                #'document_source': doc['document_source'],
                #'timestamp': doc['timestamp'],
                #'lang': doc['lang'],
                'meta': meta,
                'title': title,
                'content': content
            }
            docs_preprocessed.append(doc_preprocessed)
        
        # save extracted content
        file_out = os.path.join(out_dir,  key + '.jsonl')
        if os.path.isfile(file_out):
            os.remove(file_out)
            
        with open(file_out, 'a') as f:
            for doc in docs_preprocessed:
                f.write(json.dumps(doc) + '\n')
    print('Done')
    

#if __name__ == '__main__':
main()