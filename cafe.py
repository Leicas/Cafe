import json, npyscreen
import curses
import time
from datetime import datetime

class Listepers(npyscreen.Autocomplete):
    def set_up_handlers(self):
        super(npyscreen.Autocomplete, self).set_up_handlers()
        self.handlers.update({curses.ascii.TAB: self.auto_complete})
        self.handlers.update({curses.ascii.NL: self.auto_complete})
        self.handlers.update({curses.ascii.CR: self.auto_complete})
        self.handlers.update({"^N": self.parent.new_pack})
	self.handlers.update({"^E": self.parent.manage})
    def auto_complete(self, input):
        if self.value != "":
                possibilities = filter(lambda x: x.upper().startswith(self.value.upper()), utilisateurs)
                if len(possibilities) is 1:
                   if self.value != possibilities[0]:
                       self.value = possibilities[0]
                   else:
                        self.parent._on_ok()
                if len(possibilities) > 1:
                        self.value = possibilities[self.get_choice(possibilities)]
        self.cursor_position=len(self.value)
class TitleListepers(npyscreen.TitleText):
    _entry_type = Listepers

def affichage(user):
    sous = []
    total = 0
    for util in user['users']:
        ligne = ''
        ligne += util['name']
        ligne += " "*(12 - len(util['name']))
        ligne += '{0:+}'.format(util['account']*0.01)
        ligne += " " * (8-len('{0:+}'.format(util['account']*0.01)))
        sous.append(ligne + "Nombre de cafe:" + str(util['nombre'])+ " "*(3-len(str(util['nombre'])))+  " Dernier pris a " + datetime.fromtimestamp(util['date']).strftime("%H:%M:%S le %d/%m/%Y"))
	total = total + util['account']
    sous.append("----------")
    sous.append("Balance: " + str(-total*0.01))
    sous.append("Paquet en cours: " + str(user['current']))
    ligne = ''
    ligne += str(user['nombre']) + " cafes"
    ligne +=" en " + str(user['paquets']) + " paquets"
    sous.append(ligne)
    sous.append("Cafes par paquet: " + str((user['nombre']-user['current'])//(user['paquets']-1)))

    return sous

class manageSous(npyscreen.ActionFormMinimal):
    def set_up_handlers(self):
        super(npyscreen.ActionFormMinimal, self).set_up_handlers()
        self.handlers.update({curses.ascii.ESC:  self.parentApp.switchFormPrevious})
    def create(self):
       self.Name1 = self.add(TitleListepers, use_two_lines=True,begin_entry_at=0, name='Donneur')
       self.Name2 = self.add(TitleListepers, use_two_lines=True,begin_entry_at=0, name='Receveur')
       self.Somme = self.add(npyscreen.TitleText, use_two_lines=True,begin_entry_at=0, name="Somme")
    def new_pack(self,input):
	pass
    def manage(self,input):
        pass
    def on_ok(self):
        if self.Name1.value != "":
                user = []
                with open("user.json", "r") as data_file:
                 user = json.load(data_file)
                utilisateurs = []
                sous = []
                for util in user['users']:
                 utilisateurs.append(util['name'])
                test1 = utilisateurs.index(self.Name1.value)
                test2 = utilisateurs.index(self.Name2.value)
                user['users'][test1]['account']=user['users'][test1]['account']-int(self.Somme.value)
                user['users'][test2]['account']=user['users'][test2]['account']+int(self.Somme.value)
                with open("user.json", "w") as outfile:
                 json.dump(user, outfile, indent=4)
        self.parentApp.switchFormPrevious()
class myEmployeeForm(npyscreen.ActionFormMinimal):
    def create_control_buttons(self):
        pass
    def create(self):
       #self.Nom = self.add(npyscreen.TitleFixedText, value='Entrer le nom:')
       self.Name = self.add(TitleListepers, use_two_lines=True,begin_entry_at=0, name='Name')
       #self.Name = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Name', values = utilisateurs)
       self.Affichage = self.add(npyscreen.TitlePager, values=sous, use_two_lines=True,begin_entry_at=0, name='Comptes',editable=False)
    def manage(self,input):
        self.parentApp.getForm('MANAGESOUS').Name1.value = ''
        self.parentApp.getForm('MANAGESOUS').Name2.value = ''
        self.parentApp.getForm('MANAGESOUS').Somme.valuex = ''
        self.parentApp.switchForm('MANAGESOUS')
    def new_pack(self,input):
        user = []
        with open("user.json", "r") as data_file:
            user = json.load(data_file)
        user['paquets'] = user['paquets'] + 1
	user['current'] = 0
        sous = affichage(user)
	self.Affichage.values = sous
  	self.Affichage.display()
        with open("user.json", "w") as outfile:
          json.dump(user, outfile, indent=4)

    def on_ok(self):
        test = self.Name.value
        user = []
        with open("user.json", "r") as data_file:
            user = json.load(data_file)
        utilisateurs = []
        sous = []
        for util in user['users']:
            utilisateurs.append(util['name'])
        test = utilisateurs.index(test)
        user['users'][test]['account']=user['users'][test]['account']-user['prix']
        user['users'][test]['nombre']=user['users'][test]['nombre']+1
        user['users'][test]['date'] = time.time()
	user['nombre'] = user['nombre'] + 1
	user['current'] = user['current'] + 1
        sous = affichage(user)
        self.Affichage.values = sous
        self.Name.value = ''
        self.Affichage.display()
        with open("user.json", "w") as outfile:
          json.dump(user, outfile, indent=4)


class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', myEmployeeForm, name='Gestion du Cafe')
       self.addForm("MANAGESOUS", manageSous)
   def onInMainLoop(self):
       pass

if __name__ == '__main__':
    with open("user.json", "r") as data_file:
        user = json.load(data_file)
    utilisateurs = []
    for util in user['users']:
        utilisateurs.append(util['name'])
    sous = affichage(user)
    TestApp = MyApplication().run()



