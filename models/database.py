from tinydb import TinyDB
from tinydb import where
from tinydb import Query


class Database:
    def __init__(self, db_name) -> None:
        self.db = TinyDB(db_name)

    def save_db(self, data):

        self.db.insert(data)
        print(f"sauvegardé avec succès.")

    def update_db(self, serialized_data, ids: list, tournament=False):

        self.db.update(serialized_data, doc_ids=ids)
        if tournament == False:
            print(f"{serialized_data['name']} updaté avec succès.")
        if tournament == True:
            print(f"{serialized_data['tournament_name']} updaté avec succès.")

    def update_player_rank(self, serialized_data):
        self.db.update(
            {
                "rank": serialized_data["rank"],
                "total_score": serialized_data["total_score"],
            },
            where("name") == serialized_data["name"],
        )
        print(f"{serialized_data['name']} updaté avec succès.")

    def sorted_by(self, order):
        db_name = self.db
        reverse = False
        valid_name = ["name", "elo", "tournament_name", "elo"]
        if order not in valid_name:
            raise ValueError("Le nom du champ doit etre nom ou elo")

        if order == "elo":
            reverse = True

        data = self.get_all_data()
        return sorted(data, key=lambda doc: doc.get(order), reverse=reverse)

    def get_in_progress(self, value):
        todo = Query()
        result = self.db.search(todo.status == value)
        for record in result:
            record["id"] = record.doc_id
        return result

    def get_running_tournament(self):
        db_name = self.db
        reverse = False
        data = self.get_all_data()
        return data

    def get_element_by_id(self, id):
        record = self.db.get(doc_id=id)
        if record is not None:
            record["id"] = record.doc_id
        return record

    def get_all_data(self):
        records = self.db.all()
        for record in records:
            record["id"] = record.doc_id
        return records


if __name__ == "__main__":
    """"""
