# from FlaskWebProject1 import app
import pydocumentdb;
import pydocumentdb.document_client as document_client
from flask import Flask, render_template,request
from base64 import b64encode, b64decode
from time import time
import os
import csv


config = {
    'ENDPOINT': 'https://deepalikumar.documents.azure.com',
    'MASTERKEY': 'r5ceBO3qpnRhe9U48EcmGPKPUx6kuaM3nNPydQChNUifv260ZUxg17PGvKge3g0x0ReNDes8NqxEwQFxnkyblg==',
    'DATABASE': 'deepalidb',
    'COLLECTION': 'azuredb'
};

app = Flask(__name__)
@app.route('/')
def main():
    return render_template('documentdb.html')


@app.route('/upload', methods=['POST','GET'])
def upload():

    #  Initialize the Python DocumentDB client
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})

    # The link for database with an id of Foo would be dbs/Foo
    database_link = 'dbs/' + 'deepalidb'
    # The link for collection with an id of Bar in database Foo would be dbs/Foo/colls/Bar
    collection_link = database_link + '/colls/{0}'.format('azuredb')
    # Reading the documents in collection
    collection = client.ReadCollection(collection_link)

    # List for taking csv data
    path = '/Users/Deepali/PycharmProjects/MICROSOFT AZURE/data1'
    for filename in os.listdir(path):
        data = []

        # Splitting the file into extension
        file1, file_ext = os.path.splitext(filename)
        if file_ext == '.jpg':

            with open(path + '/' + filename, 'rb') as f:
                Imagebinaryfile = f.read()
            image = (b64encode(Imagebinaryfile)).decode('UTF-8')

            with open(path + '/' + file1 + '.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)

                # Create some documents

                doc = {}
                for i in range(0, len(data[0])):
                    try:
                        value = int(data[0][i])
                    except ValueError:
                        value = -1
                    doc.update({data[1][i].strip():value})

                document = client.CreateDocument(collection['_self'],
                                                  {
                                                      'id': file1,
                                                      'image':image,
                                                      'ingredient':doc,
                                                      'type'      :data[2][0]

                                                  })
    return ('Files uploaded successfully!')

@app.route('/download', methods=['POST','GET'])
def query():
    start = time()
    client = document_client.DocumentClient( config['ENDPOINT'], {'masterKey': config['MASTERKEY']} )
    database_link = 'dbs/' + 'deepalidb'
    collection_link = database_link + '/colls/{0}'.format('azuredb')
    collection = client.ReadCollection( collection_link )

    # Displaying all images with names
    # query = {'query': 'SELECT s.image,s.id FROM deepali s'}

    #query for displaying ingredients of a type
    # query = {'query': 'SELECT s.ingredient,s.image,s.id FROM table s where CONTAINS ( s.type ,"Snack") '}

    #query for displaying name of dish of a type
    # query = {'query': 'SELECT s.id,s.image FROM table s where CONTAINS ( s.type ,"Healthy") '}

    #query for displaying top 5 dishes
    # query = {'query': 'SELECT TOP 5 * from table s'}

    #Query for displaying contents of a single recipe
    query = {'query': 'SELECT s.image,s.id,s.type FROM deepali s where s.id = ("Tiramisu")'}

    #query for displaying the recipes with images with a specific ingredient
    # query = {'query': 'select s.id,s.image from table s where s.ingredient.Cucumber >= 0'}

    #query for count
    # query = {'query' : 'select value count(1) from s.image'}
    # query = {'query': 'select value count(1) from table s where CONTAINS (s.type ,"Healthy")'}
    # query = {'query': 'select value count(1) from table s where s.ingredient.Tomatoes >= 0'}

    options = {}
    options['enableCrossPartitionQuery'] =  True
    options['maxItemCount'] = 2
    result_iterable = client.QueryDocuments( collection['_self'], query ,options)
    value = list( result_iterable )

    # b = str(value)
    # b = value[0]

    # picture = []
    # for row in value:
    #     picture.append(row['image'])
    end = time()
    time_elap = end - start
    a = str(time_elap)

    return render_template( "imagedisplay.html", image = value ) + a
    # return str( value ) + a
    # return value[0]
    # return render_template("imagedocumentdb.html", image=picture) + a + b


if __name__ == '__main__':
    app.run(debug=True)