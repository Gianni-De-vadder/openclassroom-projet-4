from tinydb import TinyDB
from tinydb import where
class Database():

    def __init__(self, db_name ) -> None:
        if(db_name != 'players' and db_name != 'tournaments'):
            raise ValueError("La table doit être player ou tournament")

        self.db = TinyDB("data/" + db_name + ".json")   
           

    # def __init__(self) -> None:
    #     self.db = TinyDB(DATABASE_NAME)
        


    def save_db(self,data):

            # db = Connexion.TinyDB_Connect(db_name)
            self.db.insert(data)
            print(f"sauvegardé avec succès.")


    def update_db(self, serialized_data, ids: list ):

        self.db.update(serialized_data, doc_ids=ids)
        print(f"{serialized_data['name']} updaté avec succès.")


    def update_player_rank(self, serialized_data):
        self.db.update(
                {'rank': serialized_data['rank'], 'total_score': serialized_data['total_score']},
                where('name') == serialized_data['name']
        )
        print(f"{serialized_data['name']} updaté avec succès.")


    def sorted_by(self,order):
        db_name = self.db
        reverse = False
        valid_name = ['name', 'elo','tournament_name','elo']
        if order not in valid_name:
            raise ValueError('Le nom du champ doit etre nom ou elo')   

        if order == 'elo':
            reverse = True             

        data = self.get_all_data()
        return sorted(data, key = lambda doc: doc.get(order),reverse=reverse)

    def get_element_by_id(self,id):
        
        return self.db.get(doc_id=id)
        

    def get_all_data(self):
    
        records = self.db.all()
        for record in records:
            record["id"] = record.doc_id
        return records