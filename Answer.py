from __future__ import annotations
import sqlite3
from dataclasses import dataclass, field
import os
import click
import json

@dataclass
class Answer:
    conn : sqlite3.Connection
    answers : List[dict] = field(default_factory=list)

    def Loads(self) -> None:
        import importlib
        for root, dirs, files in os.walk("./Answers"):
            for f in files:
                if f == "__init__.py" or f.endswith(".pyc"):
                    continue
                answer = importlib.import_module("."+f[:-3], "Answers")
                self.answers.append({
                    "version": answer.Version,
                    "report": answer.Report,
                    "describe": answer.Describe,
                    "name": answer.Name
                })
        
    def getAnswers(self) -> Iterable[dict]:
        return self.answers
     
    def Answer(self, name : str, *args : Any) -> dict:
        for answer in self.answers:
            if answer["name"] == name:
                jsonText = answer["report"](self.conn, *args)
                return jsonText

        return "No have specify answer"