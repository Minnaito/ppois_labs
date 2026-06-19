import json
import os
from constants import RECORDS_FILE


class RecordManager:

    def __init__(self, max_records=3):
        self.max_records = max_records
        self.records = []
        self.load()

    def load(self):
        if os.path.exists(RECORDS_FILE):
            try:
                with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.records = data
                    else:
                        self.records = []
            except:
                self.records = []
        else:
            self.records = []

    def save(self):
        self.records.sort(key=lambda x: x['score'], reverse=True)
        self.records = self.records[:self.max_records]
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    def add_record(self, name, score):
        self.records.append({'name': name, 'score': score})
        self.save()
        return True

    def is_highscore(self, score):
        if len(self.records) < self.max_records:
            return True
        sorted_records = sorted(self.records, key=lambda x: x['score'], reverse=True)
        return score > sorted_records[-1]['score']

    def get_top(self, n=3):
        sorted_records = sorted(self.records, key=lambda x: x['score'], reverse=True)
        return sorted_records[:n]

    def clear_records(self):
        self.records = []
        self.save()
