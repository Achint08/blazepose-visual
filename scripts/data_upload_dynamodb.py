import boto3
import pandas

category_map_df = pandas.read_csv('excercise-category.csv')
des_df = pandas.read_csv('desciption-dataset.csv')
client = boto3.client('s3')
body = []
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('blazepose-visualization')
idx = 0
for key in client.list_objects(Bucket='blazepose-gifs')['Contents']:
    print(idx)
    idx += 1
    key = key['Key']
    name = key.replace(".gif", "")
    # print(name)
    try:
        category = category_map_df.loc[category_map_df['Name'] == name.split('_')[
            0]].iloc[0].Category
        print(category)
    except:
        continue
    if name in ["Standing Barbell Wrist Curls"]:
        continue
    description = des_df.loc[des_df['name'] ==
                             name.split('_')[0]].iloc[0].description
    exercise_key = key.replace(" ", "+")
    url = "https://blazepose-gifs.s3.us-east-2.amazonaws.com/" + exercise_key
    data = {
        'name': name,
        'category': category,
        'description': description,
        'url': url
    }
    response = table.put_item(Item=data)
    response = {"statusCode": 200, "body": json.dumps(body)}
