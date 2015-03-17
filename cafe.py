import json, npyscreen
import curses

class Listepers(npyscreen.Autocomplete):
    def set_up_handlers(self):
        super(npyscreen.Autocomplete, self).set_up_handlers()
        self.handlers.update({curses.ascii.TAB: self.auto_complete})
        self.handlers.update({curses.ascii.NL: self.auto_complete})
        self.handlers.update({curses.ascii.CR: self.auto_complete})
    def auto_complete(self, input):
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



class myEmployeeForm(npyscreen.ActionFormMinimal):
    def create_control_buttons(self):
        pass
    def create(self):
       #self.Nom = self.add(npyscreen.TitleFixedText, value='Entrer le nom:')
       self.Name = self.add(TitleListepers, use_two_lines=True,begin_entry_at=0, name='Name')
       #self.Name = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Name', values = utilisateurs)
       self.Affichage = self.add(npyscreen.TitlePager, values=sous, use_two_lines=True,begin_entry_at=0, name='Comptes',editable=False)
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
        for util in user['users']:
            sous.append(util['name'] + " " + str(util['account']*0.01))
        self.Affichage.values = sous
        self.Name.value = ''
        self.Affichage.display()
        with open("user.json", "w") as outfile:
          json.dump(user, outfile, indent=4)

        

class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', myEmployeeForm, name='Gestion du Cafe')
       # A real application might define more forms here.......
   def onInMainLoop(self):
       #with open("user.json", "r") as data_file:
        #   user = json.load(data_file)
       #user['users'][0]['account'] = user['users'][0]['account'] + 1
       pass

if __name__ == '__main__':
    with open("user.json", "r") as data_file:
        user = json.load(data_file)
    utilisateurs = []
    sous = []
    for util in user['users']:
        utilisateurs.append(util['name'])
        sous.append(util['name'] + " " + str(util['account']*0.01))
                            
    TestApp = MyApplication().run()



