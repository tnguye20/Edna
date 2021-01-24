from libs import firebase
from datetime import datetime
db = firebase.db
batch = firebase.db.batch()

class UserDao():
    def __init__(self, uid=None):
        self.ref = db.collection('users')
        self.uref = None
        self.cref = None
        if(uid):
            self.setUserRef(uid)
    
    def setUserRef(self, uid):
        self.uref = self.ref.document(uid)
        self.uid = uid

    def getUser(self, condition=None):
        data = self.uref.get()
        return {
           **data.to_dict(),
           'id': data.id
        }

    def updateUser(self, data):
        self.uref.update(data)

    def getChatHistory(self, condition=None):
        self.cref = self.uref if self.uref != None else self.uref.collection('chat')
        chat = []
        for c in self.cref.stream():
            chat.append({
                'id': c.id,
                **c.to_dict()
            })
        return chat

    def updateChatHistory(self, chat, condition=None):
        self.cref = self.uref.collection('chat')

        # Delete old chat records
        batch = firebase.db.batch()
        old_chat = self.getChatHistory() 
        for o in old_chat:
            batch.delete(self.cref.document(o.id))
        batch.commit()

        # Write new chat history
        batch = firebase.db.batch()
        cnt = 0
        for c in chat:
            c['date'] = datetime.strptime(c['date'], '%Y-%m-%d');
            c['timestamp'] = datetime.strptime(c['timestamp'], '%Y-%m-%d %H:%M:%S');
            batch.set(self.cref.document(str(cnt)), c)
            cnt = cnt + 1
        batch.commit()