from trp import Document
import json

def main():
    
    # Enter the path of the AnalyzeDocResponsejson or the Textractdumpresponse They are the same thing!
    response = open("//PATH TO JSON FILE")  
    data = json.load(response)

    # Creating instance of TRP Document
    doc = Document(data)  
    
    #Now we can check every page and extract the table rows and the key value pairs
    for page in doc.pages:

        # Print tables
        for table in page.tables:
            for row in table.rows:
                print(row)
                print("\n")
                
            
        # Print all the fields
        for field in page.form.fields:
                    if field.key and field.value:
                        print("Field: Key: {}, Value: {}".format(field.key.text, field.value.text))

        # Search fields by key. Here we search for the keyword Aris. We get the form value. We can do the same for student name, lesson number,etc
        key = "ARIS"
        fields = page.form.searchFieldsByKey(key)
        for field in fields:
            print("Searching the fields by Key the value Field: Key: {}   , Value: {}".format(field.key, field.value))
        





if __name__ == "__main__":
    main()
