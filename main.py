import cx_Oracle
import datetime
import tkinter as tk

#Au fost testate toate functionalitatile
def display_window(mode, text, user_input):
    # Create the main window
    root = tk.Tk()
    root.title("Window")
   # root.after(1, lambda: root.focus_force())
    # Set the window size
    root.geometry("600x200")

    # Set the window to be resizeable
    root.resizable(True, True)

    # Display text
    if mode == "text":
        label = tk.Label(root, text=text)
        label.pack()
        root.update_idletasks()
        root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")
    # Get user input
    elif mode == "input":
        # Create label with text
        label = tk.Label(root, text=text)
        label.pack()

        # Create text box
        entry = tk.Entry(root)
        entry.pack()
        entry.focus_force()
        # Create submit button
        def submit():
            user_input.append(entry.get())
            root.destroy()

        button = tk.Button(root, text="Submit", command=submit)
        button.pack()
        root.update_idletasks()
        root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")
        root.bind("<Return>", lambda event: submit())
    # Run the main loop
    root.mainloop()

con = cx_Oracle.connect("rares", "rares", "localhost/xe")
def initializare():
    print('Initializare')
    f = open('script_introducere_date.sql')
    exp = con.cursor()
    full_sql = f.read()
    sql_commands = full_sql.split(';')
    try:
       for sql_command in sql_commands:
           if sql_command!='':
            exp.execute(sql_command)
    except cx_Oracle.DatabaseError:
        print(sql_command)
    exp.close()
def afisare_produse(text_initial):
    exp = con.cursor()
    text_de_afisat = text_initial
    exp.execute(
        'SELECT p.CAR_P,sp.NUME_STARE,tp.NUME_TIP_PRODUS,np.NUME_FIRMA FROM PRODUSE p,STARE_PRODUS sp,TIP_PRODUS tp,NUME_PRODUCATOR np WHERE p.STARE_PRODUS_ID_STARE=sp.ID_STARE and p.NUME_PRODUCATOR_ID_FIRMA=np.ID_FIRMA and p.TIP_PRODUS_ID_PRODUS=tp.ID_PRODUS')
    for result in exp:
        text_de_afisat += str(result) + '\n'
    display_window('text', text_de_afisat, [])
def afisare_magazie(text_initial):
    exp = con.cursor()
    text_de_afisat = text_initial
    exp.execute(
        'SELECT p.CAR_P,sp.NUME_STARE,tp.NUME_TIP_PRODUS,np.NUME_FIRMA,m.CANTITATE_DISPONIBILA,m.PRET FROM PRODUSE p,STARE_PRODUS sp,TIP_PRODUS tp,NUME_PRODUCATOR np,MAGAZIE m WHERE p.STARE_PRODUS_ID_STARE=sp.ID_STARE and p.NUME_PRODUCATOR_ID_FIRMA=np.ID_FIRMA and p.TIP_PRODUS_ID_PRODUS=tp.ID_PRODUS and p.ID_P_CR=m.PRODUSE_ID_P_CR')
    for result in exp:
        text_de_afisat += str(result) + '\n'
    display_window('text', text_de_afisat, [])
def afisare_vanzari(text_initial):
    exp = con.cursor()
    text_de_afisat = text_initial
    exp.execute(
        'SELECT p.CAR_P,sp.NUME_STARE,tp.NUME_TIP_PRODUS,np.NUME_FIRMA,v.CANTITATE_DORITA,v.data FROM PRODUSE p,STARE_PRODUS sp,TIP_PRODUS tp,NUME_PRODUCATOR np,VANZARI v WHERE p.STARE_PRODUS_ID_STARE=sp.ID_STARE and p.NUME_PRODUCATOR_ID_FIRMA=np.ID_FIRMA and p.TIP_PRODUS_ID_PRODUS=tp.ID_PRODUS and p.ID_P_CR=v.PRODUSE_ID_P_CR')
    for result in exp:
        text_de_afisat += str(result) + '\n'
    display_window('text', text_de_afisat, [])
def afisare_tabela():
    tab=[]
    display_window('input','Tabelele disponibile sunt magazie, vanzari, tip_produs, stare_produs, produse si nume_producator\nIntroduceti numele tabelei de vazut:',tab)
    exp = con.cursor()
    try:
        tab[0]=tab[0].lower()
        if tab[0]=='magazie':
            afisare_magazie('')
        elif tab[0]=='produse':
                afisare_produse('')
        elif tab[0]=='vanzari':
            afisare_vanzari('')
        else:
            text_de_afisat=''
            exp.execute('select * from '+tab[0])
            for result in exp:
                text_de_afisat+=str(result)+'\n'
            display_window('text',text_de_afisat,[])
    except cx_Oracle.DatabaseError:
        display_window('text', 'Tabela introdusa nu exista', [])
    except IndexError:
        pass
    exp.close()
def adaugare_in_tabela():
    try:
        lista = []
        display_window('input','Tabelele disponibile sunt magazie, vanzari, tip_produs, stare_produs, produse si nume_producator\nIntroduceti numele tabelei in care se adauga:',lista)
        if lista!=[]:
            tab = lista[0]
            tab=tab.lower()
            exp=con.cursor()
            if(tab=='tip_produs'):
                lista=[]
                display_window('input','Numele tipului de produs de inserat:',lista)
                if lista!=[]:
                    tip_produs_de_inserat=lista[0]
                    exp.execute("INSERT INTO TIP_PRODUS(NUME_TIP_PRODUS) VALUES(\'"+tip_produs_de_inserat+"\')")
                    exp.execute('select * from TIP_PRODUS')
                    text_de_afisat = "Tabela modificata:\n"
                    for result in exp:
                        text_de_afisat+=str(result)+'\n'
                    display_window('text',text_de_afisat,[])
            elif(tab=='stare_produs'):
                lista = []
                display_window('input', 'Numele starii de produs de inserat:', lista)
                if lista != []:
                    stare_produs_de_inserat=lista[0]
                    exp.execute("INSERT INTO STARE_PRODUS(NUME_STARE) VALUES(\'" + stare_produs_de_inserat + "\')")
                    exp.execute('select * from STARE_PRODUS')
                    text_de_afisat = "Tabela modificata:\n"
                    for result in exp:
                        text_de_afisat += str(result) + '\n'
                    display_window('text', text_de_afisat, [])
            elif(tab=='nume_producator'):
               lista = []
               display_window('input', 'Numele producatorului de inserat:', lista)
               if lista != []:
                    nume_prod_de_inserat = lista[0]
                    exp.execute("INSERT INTO NUME_PRODUCATOR(NUME_FIRMA) VALUES(\'" + nume_prod_de_inserat  + "\')")
                    exp.execute('select * from nume_producator')
                    text_de_afisat = "Tabela modificata:\n"
                    for result in exp:
                        text_de_afisat += str(result) + '\n'
                    display_window('text', text_de_afisat, [])
            elif(tab=='produse'):
                lista = []
                display_window('input','Caracteristica produsului de inserat:',lista)
                caracteristica=lista[0].lower()
                lista_firme = []
                lista = []
                exp.execute("SELECT nume_firma from nume_producator")
                text_de_afisat = "Alegeti o firma din cele de mai jos:\n"
                for result in exp:
                    text_de_afisat += str(result[0]) + '\n'
                    lista_firme.append(result[0].lower())
                text_de_afisat += 'Firma aleasa:\n'
                display_window('input', text_de_afisat, lista)
                firma_aleasa = lista[0].lower()
                while firma_aleasa not in lista_firme:
                    lista=[]
                    display_window('input', text_de_afisat, lista)
                    firma_aleasa = lista[0].lower()
                lista = []
                lista_tipuri1 = []
                lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
                exp.execute("SELECT nume_tip_produs from tip_produs")
                for result in exp:
                    lista_tipuri1.append(result[0].lower())
                    lista_tipuri += str(result[0]) + '\n'
                lista_tipuri += 'Tip de produs ales:'
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
                while tip_produs_ales not in lista_tipuri1:
                    lista = []
                    display_window('input', lista_tipuri, lista)
                    tip_produs_ales = lista[0].lower()
                lista = []
                text1 = "Alegeti o stare de produs din cele de mai jos:\n"
                lista_stari = []
                exp.execute("SELECT nume_stare from stare_produs")
                for result in exp:
                    text1 += str(result[0]) + '\n'
                    lista_stari.append(result[0].lower())
                text1 += 'Stare aleasa:'
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
                while stare_aleasa not in lista_stari:
                    lista = []
                    display_window('input', text1, lista)
                    stare_aleasa = lista[0].lower()
                exp.execute('INSERT INTO PRODUSE(TIP_PRODUS_ID_PRODUS,CAR_P,NUME_PRODUCATOR_ID_FIRMA,STARE_PRODUS_ID_STARE) VALUES((SELECT ID_PRODUS FROM tip_produs WHERE NUME_TIP_PRODUS LIKE \''+tip_produs_ales+'\'),\''+caracteristica+'\',(SELECT ID_firma FROM nume_producator WHERE NUME_FIRMA LIKE \''+firma_aleasa+'\'),(SELECT ID_STARE FROM STARE_PRODUS WHERE NUME_STARE LIKE \''+stare_aleasa+'\'))')
                text_de_afisat = "Tabela modificata:\n"
                afisare_produse(text_de_afisat)
            elif tab=='magazie':
                lista = []
                lista_caracteristici = []
                exp.execute("SELECT car_p from produse")
                text_de_afisat = "Alegeti o caracteristica din cele de mai jos:"
                for result in exp:
                    text_de_afisat += str(result[0]) + '\n'
                    lista_caracteristici.append(result[0].lower())
                text_de_afisat += 'Caracteristica produsului de inserat:\n'
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
                while caracteristica not in lista_caracteristici:
                    lista = []
                    display_window('input', text_de_afisat, lista)
                    caracteristica = lista[0].lower()
                lista_firme = []
                lista = []
                exp.execute("SELECT nume_firma from nume_producator")
                text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
                for result in exp:
                    text_de_afisat_f += str(result[0]) + '\n'
                    lista_firme.append(result[0].lower())
                text_de_afisat_f += 'Firma aleasa:\n'
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
                while firma_aleasa not in lista_firme:
                    lista = []
                    display_window('input', text_de_afisat_f, lista)
                    firma_aleasa = lista[0]
                lista = []
                lista_tipuri1 = []
                lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
                exp.execute("SELECT nume_tip_produs from tip_produs")
                for result in exp:
                    lista_tipuri1.append(result[0].lower())
                    lista_tipuri += str(result[0]) + '\n'
                lista_tipuri += 'Tip de produs ales:'
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
                while tip_produs_ales not in lista_tipuri1:
                    lista = []
                    display_window('input', lista_tipuri, lista)
                    tip_produs_ales = lista[0].lower()
                lista = []
                text1 = "Alegeti o stare de produs din cele de mai jos:\n"
                lista_stari = []
                exp.execute("SELECT nume_stare from stare_produs")
                for result in exp:
                    text1 += str(result[0]) + '\n'
                    lista_stari.append(result[0])
                text1 += 'Stare aleasa:'
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
                while stare_aleasa not in lista_stari:
                    lista = []
                    display_window('input', text1, lista)
                    stare_aleasa = lista[0].lower()
                #De cautat produsul in produse
                exp.execute("(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'"+tip_produs_ales+"\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'"+firma_aleasa+"\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'"+stare_aleasa+"\' and produse.car_p=\'"+caracteristica+"\' )")
                for result in exp:
                    lista=[]
                    display_window('input','Cantitatea disponibila pentru produsul cu id-ul '+str(result[0])+':',lista)
                    cantitate_disponibila=lista[0]
                    lista = []
                    display_window('input','Pretul pentru produsul cu id-ul '+str(result[0])+':',lista)
                    pret=lista[0]
                    try:
                        exp1=con.cursor()
                        exp1.execute('INSERT INTO MAGAZIE(magazie.produse_id_p_cr,CANTITATE_DISPONIBILA,PRET) VALUES('+str(result[0])+','+str(cantitate_disponibila)+','+str(pret)+')')
                        text_de_afisat = "Tabela modificata:\n"
                        afisare_magazie(text_de_afisat)
                    except cx_Oracle.IntegrityError or cx_Oracle.DatabaseError or cx_Oracle.InterfaceError:
                        display_window('text','Produsul deja exista in magazie',[])
            elif tab=='vanzari':
                lista = []
                lista_caracteristici = []
                exp.execute("SELECT car_p from produse")
                text_de_afisat = "Alegeti o caracteristica din cele de mai jos:"
                for result in exp:
                    text_de_afisat += str(result[0]) + '\n'
                    lista_caracteristici.append(result[0].lower())
                text_de_afisat += 'Caracteristica produsului de inserat:\n'
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
                while caracteristica not in lista_caracteristici:
                    lista = []
                    display_window('input', text_de_afisat, lista)
                    caracteristica = lista[0].lower()
                lista_firme = []
                lista = []
                exp.execute("SELECT nume_firma from nume_producator")
                text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
                for result in exp:
                    text_de_afisat_f += str(result[0]) + '\n'
                    lista_firme.append(result[0].lower())
                text_de_afisat_f += 'Firma aleasa:\n'
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
                while firma_aleasa not in lista_firme:
                    lista = []
                    display_window('input', text_de_afisat_f, lista)
                    firma_aleasa = lista[0]
                lista = []
                lista_tipuri1 = []
                lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
                exp.execute("SELECT nume_tip_produs from tip_produs")
                for result in exp:
                    lista_tipuri1.append(result[0].lower())
                    lista_tipuri += str(result[0]) + '\n'
                lista_tipuri += 'Tip de produs ales:'
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
                while tip_produs_ales not in lista_tipuri1:
                    lista = []
                    display_window('input', lista_tipuri, lista)
                    tip_produs_ales = lista[0].lower()
                lista = []
                text1 = "Alegeti o stare de produs din cele de mai jos:\n"
                lista_stari = []
                exp.execute("SELECT nume_stare from stare_produs")
                for result in exp:
                    text1 += str(result[0]) + '\n'
                    lista_stari.append(result[0])
                text1 += 'Stare aleasa:'
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
                while stare_aleasa not in lista_stari:
                    lista = []
                    display_window('input', text1, lista)
                    stare_aleasa = lista[0].lower()
                # De cautat produsul in produse
                exp.execute(
                    "(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'" + tip_produs_ales + "\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'" + firma_aleasa + "\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'" + stare_aleasa + "\' and produse.car_p=\'" + caracteristica + "\' )")
                for result in exp:
                    lista=[]
                    display_window('input','Cantitatea dorita pentru produsul cu id-ul ' + str(result[0]) + ':',lista)
                    cantitate_dorita = lista[0]
                    lista = []
                    display_window('input', 'Data vanzarii pentru produsul cu id-ul ' + str(result[0]) + '(format:DD-MMM-YY):', lista)
                    data = lista[0]
                    exp1=con.cursor()
                    try:
                        exp1.execute("BEGIN INSERT INTO VANZARI(produse_id_p_cr,cantitate_dorita,data) VALUES("+str(result[0])+","+cantitate_dorita+",'"+data+"');UPDATE MAGAZIE SET CANTITATE_DISPONIBILA=CANTITATE_DISPONIBILA-"+cantitate_dorita+" where PRODUSE_ID_P_CR="+str(result[0])+";COMMIT; END;")
                    except cx_Oracle.DatabaseError:
                        display_window('text', 'Datele introduse au fost incorecte, se reia de la inceput', [])
                text_de_afisat = "Tabela modificata:\n"
                afisare_vanzari(text_de_afisat)
    except cx_Oracle.IntegrityError or cx_Orac.DatabaseError:
        display_window('text','Datele introduse au fost incorecte, se reia de la inceput',[])
    except IndexError:
        pass
    finally:
        exp.close()
def stergere():
    try:
        lista = []
        display_window('input','Tabelele disponibile sunt magazie, vanzari, tip_produs, stare_produs, produse si nume_producator\nIntroduceti numele tabelei in care se sterge:',lista)
        tab=lista[0]
        exp = con.cursor()
        if tab=='vanzari':
            lista = []
            lista_caracteristici = []
            exp.execute("SELECT car_p from produse")
            text_de_afisat = "Alegeti o caracteristica din cele de mai jos:"
            for result in exp:
                text_de_afisat += str(result[0]) + '\n'
                lista_caracteristici.append(result[0].lower())
            text_de_afisat += 'Caracteristica produsului:\n'
            display_window('input', text_de_afisat, lista)
            caracteristica = lista[0].lower()
            while caracteristica not in lista_caracteristici:
                lista = []
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
            lista_firme = []
            lista = []
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat_f += str(result[0]) + '\n'
                lista_firme.append(result[0].lower())
            text_de_afisat_f += 'Firma aleasa:'
            display_window('input', text_de_afisat_f, lista)
            firma_aleasa = lista[0]
            while firma_aleasa not in lista_firme:
                lista = []
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
            lista = []
            lista_tipuri1 = []
            lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri += str(result[0]) + '\n'
            lista_tipuri += 'Tip de produs ales:'
            display_window('input', lista_tipuri, lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
            lista = []
            text1 = "Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1 += str(result[0]) + '\n'
                lista_stari.append(result[0])
            text1 += 'Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            # De cautat produsul in produse
            exp.execute(
                "(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'" + tip_produs_ales + "\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'" + firma_aleasa + "\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'" + stare_aleasa + "\' and produse.car_p=\'" + caracteristica + "\' )")
            for result in exp:
                exp1 = con.cursor()
                exp1.execute('SELECT cantitate_disponibila FROM MAGAZIE WHERE produse_id_p_cr=' + str(result[0]))
                exp2 = con.cursor()
                exp3=con.cursor()
                for result1 in exp1:
                    lista=[]
                    display_window('input',"Cantitatea vanzarii de sters:",lista)
                    cantitate_de_sters =lista[0]
                    lista = []
                    display_window('input', 'Data vanzarii pentru produsul cu id-ul ' + str(result[0]) + ' de sters(format:DD-MMM-YY):', lista)
                    data_de_sters =lista[0]
                    exp2.execute("SELECT cantitate_dorita FROM VANZARI WHERE produse_id_p_cr="+str(result[0])+' and cantitate_dorita='+cantitate_de_sters+" and data='"+data_de_sters+"'")
                    for result2 in exp2:
                       exp3.execute("UPDATE MAGAZIE set CANTITATE_DISPONIBILA=CANTITATE_DISPONIBILA+"+str(result2[0])+" where PRODUSE_ID_P_CR="+str(result[0]))
                       exp3.execute('DELETE FROM VANZARI WHERE produse_id_p_cr=' + str(result[0])+' and cantitate_dorita='+cantitate_de_sters+" and data='"+data_de_sters+"'")
                    text_de_afisat = "Tabela modificata:\n"
                    afisare_vanzari(text_de_afisat)
        elif tab=='produse':
            lista = []
            lista_caracteristici = []
            exp.execute("SELECT car_p from produse")
            text_de_afisat = "Alegeti o caracteristica din cele de mai jos:\n"
            for result in exp:
                text_de_afisat += str(result[0]) + '\n'
                lista_caracteristici.append(result[0].lower())
            text_de_afisat += 'Caracteristica produsului de inserat:\n'
            display_window('input', text_de_afisat, lista)
            caracteristica = lista[0].lower()
            while caracteristica not in lista_caracteristici:
                lista = []
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
            lista_firme = []
            lista = []
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat_f += str(result[0]) + '\n'
                lista_firme.append(result[0].lower())
            text_de_afisat_f += 'Firma aleasa:'
            display_window('input', text_de_afisat_f, lista)
            firma_aleasa = lista[0]
            while firma_aleasa not in lista_firme:
                lista = []
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
            lista = []
            lista_tipuri1 = []
            lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri += str(result[0]) + '\n'
            lista_tipuri += 'Tip de produs ales:'
            display_window('input', lista_tipuri, lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
            lista = []
            text1 = "Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1 += str(result[0]) + '\n'
                lista_stari.append(result[0])
            text1 += 'Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            # De cautat produsul in produse
            exp.execute(
                "(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'" + tip_produs_ales + "\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'" + firma_aleasa + "\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'" + stare_aleasa + "\' and produse.car_p=\'" + caracteristica + "\' )")
            for result in exp:
                exp1=con.cursor()
                exp1.execute("DELETE FROM MAGAZIE WHERE PRODUSE_ID_P_CR="+str(result[0]))
                exp1.execute("DELETE FROM VANZARI WHERE PRODUSE_ID_P_CR="+str(result[0]))
                exp1.execute("DELETE FROM PRODUSE WHERE ID_P_CR="+str(result[0]))
            text_de_afisat = "Tabela modificata:\n"
            afisare_produse(text_de_afisat)
        elif tab=='magazie':
            lista = []
            lista_caracteristici = []
            exp.execute("SELECT car_p from produse")
            text_de_afisat = "Alegeti o caracteristica din cele de mai jos:"
            for result in exp:
                text_de_afisat += str(result[0]) + '\n'
                lista_caracteristici.append(result[0].lower())
            text_de_afisat += 'Caracteristica produsului de inserat:\n'
            display_window('input', text_de_afisat, lista)
            caracteristica = lista[0].lower()
            while caracteristica not in lista_caracteristici:
                lista = []
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
            lista_firme = []
            lista = []
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat_f += str(result[0]) + '\n'
                lista_firme.append(result[0].lower())
            text_de_afisat_f += 'Firma aleasa:'
            display_window('input', text_de_afisat_f, lista)
            firma_aleasa = lista[0]
            while firma_aleasa not in lista_firme:
                lista = []
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
            lista = []
            lista_tipuri1 = []
            lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri += str(result[0]) + '\n'
            lista_tipuri += 'Tip de produs ales:'
            display_window('input', lista_tipuri, lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
            lista = []
            text1 = "Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1 += str(result[0]) + '\n'
                lista_stari.append(result[0])
            text1 += 'Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            # De cautat produsul in produse
            exp.execute(
                "(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'" + tip_produs_ales + "\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'" + firma_aleasa + "\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'" + stare_aleasa + "\' and produse.car_p=\'" + caracteristica + "\' )")
            for result in exp:
                exp1 = con.cursor()
                exp1.execute("DELETE FROM MAGAZIE WHERE PRODUSE_ID_P_CR=" + str(result[0]))
                exp1.execute("DELETE FROM VANZARI WHERE PRODUSE_ID_P_CR=" + str(result[0]))
            text_de_afisat = "Tabela modificata:\n"
            afisare_magazie(text_de_afisat)
        elif tab=='tip_produs':
            lista=[]
            lista_tipuri1 = []
            lista_tipuri="Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri+=str(result[0])+'\n'
            lista_tipuri+='Tip de produs ales:'
            display_window('input',lista_tipuri,lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input',lista_tipuri,lista)
                tip_produs_ales = lista[0].lower()
            exp.execute("SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS WHERE PRODUSE.tip_produs_id_produs=TIP_PRODUS.id_produs and TIP_PRODUS.nume_tip_produs='"+tip_produs_ales+"'")
            for result in exp:
                exp1=con.cursor()
                exp1.execute("DELETE FROM MAGAZIE WHERE PRODUSE_ID_P_CR=" + str(result[0]))
                exp1.execute("DELETE FROM VANZARI WHERE PRODUSE_ID_P_CR=" + str(result[0]))
                exp1.execute("DELETE FROM PRODUSE WHERE ID_P_CR=" + str(result[0]))
            exp.execute("DELETE FROM TIP_PRODUS WHERE nume_tip_produs='"+tip_produs_ales+"'")
            exp.execute('SELECT * FROM TIP_PRODUS')
            text_de_afisat = "Tabela modificata:\n"
            for result in exp:
                text_de_afisat += str(result) + '\n'
            display_window('text', text_de_afisat, [])
        elif tab=='stare_produs':
            lista=[]
            text1="Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1+=str(result[0])+'\n'
                lista_stari.append(result[0])
            text1+='Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            exp.execute(
                "SELECT ID_P_CR FROM PRODUSE,STARE_PRODUS WHERE PRODUSE.stare_produs_id_stare=STARE_PRODUS.id_stare and STARE_PRODUS.nume_stare='" + stare_aleasa + "'")
            for result in exp:
                exp1 = con.cursor()
                exp1.execute("DELETE FROM MAGAZIE WHERE PRODUSE_ID_P_CR=" + str(result[0]))
                exp1.execute("DELETE FROM VANZARI WHERE PRODUSE_ID_P_CR=" + str(result[0]))
                exp1.execute("DELETE FROM PRODUSE WHERE ID_P_CR=" + str(result[0]))
            exp.execute("DELETE FROM STARE_PRODUS WHERE nume_stare='" + stare_aleasa + "'")
            exp.execute('SELECT * FROM STARE_PRODUS')
            text_de_afisat = "Tabela modificata:\n"
            for result in exp:
                text_de_afisat += str(result) + '\n'
            display_window('text', text_de_afisat, [])
        elif tab=='nume_producator':
            lista_firme = []
            lista = []
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat = "Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat += str(result[0]) + '\n'
                lista_firme.append(result[0].lower())
            text_de_afisat += 'Firma aleasa pentru sters:\n'
            display_window('input', text_de_afisat, lista)
            firma_aleasa = lista[0]
            exp.execute(
                "SELECT ID_P_CR FROM PRODUSE,NUME_PRODUCATOR WHERE PRODUSE.nume_producator_id_firma=NUME_PRODUCATOR.id_firma and NUME_PRODUCATOR.nume_firma='" + firma_aleasa + "'")
            for result in exp:
                exp1 = con.cursor()
                exp1.execute("DELETE FROM MAGAZIE WHERE PRODUSE_ID_P_CR=" + str(result[0]))
                exp1.execute("DELETE FROM VANZARI WHERE PRODUSE_ID_P_CR=" + str(result[0]))
                exp1.execute("DELETE FROM PRODUSE WHERE ID_P_CR=" + str(result[0]))
            exp.execute("DELETE FROM NUME_PRODUCATOR WHERE nume_firma='" + firma_aleasa + "'")
            exp.execute('SELECT * FROM NUME_PRODUCATOR')
            text_de_afisat = "Tabela modificata:\n"
            for result in exp:
                text_de_afisat += str(result) + '\n'
            display_window('text', text_de_afisat, [])
    except cx_Oracle.IntegrityError:
            display_window('text', 'Datele introduse au fost incorecte, se reia de la inceput', [])
    except IndexError:
        pass
    finally:
        exp.close()
def modificare():
    try:
        lista = []
        display_window('input','Tabelele disponibile sunt magazie, vanzari, tip_produs, stare_produs, produse si nume_producator\nIntroduceti numele tabelei care se modifica:',lista)
        tab = lista[0]
        exp = con.cursor()
        if tab == 'nume_producator':
            lista_firme = []
            lista=[]
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat="Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat+=str(result[0])+'\n'
                lista_firme.append(result[0].lower())
            text_de_afisat+='Firma aleasa:'
            display_window('input',text_de_afisat,lista)
            firma_aleasa = lista[0]
            while firma_aleasa not in lista_firme:
                lista = []
                display_window('input', text_de_afisat, lista)
                firma_aleasa = lista[0]
            lista=[]
            display_window('input','Noul nume pentru firma:', lista)
            nume_nou_firma=lista[0]
            exp.execute("UPDATE NUME_PRODUCATOR SET nume_producator.nume_firma='"+nume_nou_firma+"' where nume_producator.nume_firma='"+firma_aleasa+"'")
            exp.execute('SELECT * FROM NUME_PRODUCATOR')
            text_de_afisat = "Tabela modificata:\n"
            for result in exp:
                text_de_afisat += str(result) + '\n'
            display_window('text', text_de_afisat, [])
        elif tab=='stare_produs':
            lista = []
            text1 = "Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1 += str(result[0]) + '\n'
                lista_stari.append(result[0])
            text1 += 'Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            lista=[]
            display_window('input', 'Numele nou pentru starea aleasa:', lista)
            nume_nou_stare=lista[0]
            exp.execute("UPDATE STARE_PRODUS SET stare_produs.nume_stare='" + nume_nou_stare + "' where stare_produs.nume_stare='" + stare_aleasa + "'")
            exp.execute('SELECT * FROM STARE_PRODUS')
            text_de_afisat = "Tabela modificata:\n"
            for result in exp:
                text_de_afisat += str(result) + '\n'
            display_window('text', text_de_afisat, [])
        elif tab=='tip_produs':
            lista = []
            lista_tipuri1 = []
            lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri += str(result[0]) + '\n'
            lista_tipuri += 'Tip de produs ales:'
            display_window('input', lista_tipuri, lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
            lista=[]
            display_window('input',"Numele nou pentru tipul de produs ales:",lista)
            nume_nou_tip_produs=lista[0]
            exp.execute("UPDATE TIP_PRODUS SET nume_tip_produs='" + nume_nou_tip_produs + "' where nume_tip_produs='" + tip_produs_ales + "'")
            exp.execute('SELECT * FROM TIP_PRODUS')
            text_de_afisat = "Tabela modificata:\n"
            for result in exp:
                text_de_afisat += str(result) + '\n'
            display_window('text', text_de_afisat, [])
        elif tab=='produse':
            lista=[]
            lista_caracteristici = []
            exp.execute("SELECT car_p from produse")
            text_de_afisat="Alegeti o caracteristica din cele de mai jos:\n"
            for result in exp:
                text_de_afisat+=str(result[0])+'\n'
                lista_caracteristici.append(result[0].lower())
            text_de_afisat+='Caracteristica produsului de inserat:\n'
            display_window('input',text_de_afisat,lista)
            caracteristica = lista[0].lower()
            while caracteristica not in lista_caracteristici:
                lista = []
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
            lista_firme = []
            lista = []
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat_f += str(result[0]) + '\n'
                lista_firme.append(result[0].lower())
            text_de_afisat_f += 'Firma aleasa:'
            display_window('input', text_de_afisat_f, lista)
            firma_aleasa = lista[0]
            while firma_aleasa not in lista_firme:
                lista = []
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
            lista = []
            lista_tipuri1 = []
            lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri += str(result[0]) + '\n'
            lista_tipuri += 'Tip de produs ales:'
            display_window('input', lista_tipuri, lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
            lista = []
            text1 = "Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1 += str(result[0]) + '\n'
                lista_stari.append(result[0])
            text1 += 'Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            # De cautat produsul in produse
            exp.execute(
                "(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'" + tip_produs_ales + "\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'" + firma_aleasa + "\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'" + stare_aleasa + "\' and produse.car_p=\'" + caracteristica + "\' )")
            for result in exp:
                exp1 = con.cursor()
                lista_optiuni = ['caracteristica', 'nume_producator', 'tip_produs', 'stare_produs']
                lista=[]
                display_window('input',"Ce doriti sa modificati? Optiune(caracteristica,nume_producator,tip_produs,stare_produs:",lista)
                optiune_modificare=lista[0]
                while optiune_modificare not in lista_optiuni:
                    lista = []
                    display_window('input',"Ce doriti sa modificati? Optiune(caracteristica,nume_producator,tip_produs,stare_produs:",lista)
                    optiune_modificare = lista[0]
                if optiune_modificare=='caracteristica':
                    lista=[]
                    display_window('input','Introduceti noua caracteristica:',lista)
                    caracteristica_noua=lista[0]
                    exp1.execute("UPDATE PRODUSE SET car_p ='"+caracteristica_noua+"' WHERE id_p_cr="+str(result[0]))
                elif optiune_modificare=='nume_producator':
                    lista = []
                    display_window('input',text_de_afisat_f, lista)
                    nume_producator_nou=lista[0]
                    while nume_producator_nou not in lista_firme:
                        lista = []
                        display_window('input', text_de_afisat_f, lista)
                        nume_producator_nou = lista[0]
                    exp1.execute("UPDATE PRODUSE SET nume_producator_id_firma = (SELECT ID_FIRMA FROM NUME_PRODUCATOR WHERE NUME_FIRMA='"+nume_producator_nou+"') WHERE id_p_cr="+str(result[0]))
                elif optiune_modificare=='tip_produs':
                    lista = []
                    display_window('input', lista_tipuri, lista)
                    nume_producator_nou = lista[0]
                    while nume_producator_nou not in lista_tipuri1:
                        lista = []
                        display_window('input', "Noul tip al produsului:", lista)
                        nume_producator_nou = lista[0]
                    exp1.execute("UPDATE PRODUSE SET tip_produs_id_produs  = (SELECT ID_PRODUS FROM TIP_PRODUS WHERE nume_tip_produs='" + nume_producator_nou + "') WHERE id_p_cr=" + str(result[0]))
                elif optiune_modificare=='stare_produs':
                    lista = []
                    display_window('input', text1, lista)
                    nume_producator_nou = lista[0]
                    while nume_producator_nou not in lista_stari:
                        lista = []
                        display_window('input', "Noua stare a produsului:", lista)
                        nume_producator_nou = lista[0]
                    exp1.execute("UPDATE PRODUSE SET stare_produs_id_stare  = (SELECT ID_STARE FROM STARE_PRODUS WHERE nume_stare='" + nume_producator_nou + "') WHERE id_p_cr=" + str(result[0]))
            text_de_afisat = "Tabela modificata:\n"
            afisare_produse(text_de_afisat)
        elif tab=='magazie':
            lista = []
            lista_caracteristici = []
            exp.execute("SELECT car_p from produse")
            text_de_afisat = "Alegeti o caracteristica din cele de mai jos:\n"
            for result in exp:
                text_de_afisat += str(result[0]) + '\n'
                lista_caracteristici.append(result[0].lower())
            text_de_afisat += 'Caracteristica produsului de inserat:\n'
            display_window('input', text_de_afisat, lista)
            caracteristica = lista[0].lower()
            while caracteristica not in lista_caracteristici:
                lista = []
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
            lista_firme = []
            lista = []
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat_f += str(result[0]) + '\n'
                lista_firme.append(result[0].lower())
            text_de_afisat_f += 'Firma aleasa:'
            display_window('input', text_de_afisat_f, lista)
            firma_aleasa = lista[0]
            while firma_aleasa not in lista_firme:
                lista = []
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
            lista = []
            lista_tipuri1 = []
            lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri += str(result[0]) + '\n'
            lista_tipuri += 'Tip de produs ales:'
            display_window('input', lista_tipuri, lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
            lista = []
            text1 = "Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1 += str(result[0]) + '\n'
                lista_stari.append(result[0])
            text1 += 'Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            # De cautat produsul in produse
            exp.execute(
                "(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'" + tip_produs_ales + "\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'" + firma_aleasa + "\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'" + stare_aleasa + "\' and produse.car_p=\'" + caracteristica + "\' )")
            for result in exp:
                exp1 = con.cursor()
                lista=[]
                display_window('input','Cantitatea cea noua pentru produsul cu id '+str(result[0])+' din magazie:',lista)
                cantitate_noua=lista[0]
                lista = []
                display_window('input','Pretul cel nou pentru produsul cu id '+str(result[0])+' din magazie:',lista)
                pret_nou=lista[0]
                if cantitate_noua!='':
                    exp1.execute("UPDATE MAGAZIE SET cantitate_disponibila="+cantitate_noua+" where produse_id_p_cr="+str(result[0]))
                if pret_nou!='':
                    exp1.execute("UPDATE MAGAZIE SET pret=" + pret_nou + " where produse_id_p_cr=" + str(result[0]))
            text_de_afisat = "Tabela modificata:\n"
            afisare_magazie(text_de_afisat)
        elif tab=='vanzari':
            lista = []
            lista_caracteristici = []
            exp.execute("SELECT car_p from produse")
            text_de_afisat = "Alegeti o caracteristica din cele de mai jos:\n"
            for result in exp:
                text_de_afisat += str(result[0]) + '\n'
                lista_caracteristici.append(result[0].lower())
            text_de_afisat += 'Caracteristica produsului de inserat:\n'
            display_window('input', text_de_afisat, lista)
            caracteristica = lista[0].lower()
            while caracteristica not in lista_caracteristici:
                lista = []
                display_window('input', text_de_afisat, lista)
                caracteristica = lista[0].lower()
            lista_firme = []
            lista = []
            exp.execute("SELECT nume_firma from nume_producator")
            text_de_afisat_f = "Alegeti o firma din cele de mai jos:\n"
            for result in exp:
                text_de_afisat_f += str(result[0]) + '\n'
                lista_firme.append(result[0].lower())
            text_de_afisat_f += 'Firma aleasa:'
            display_window('input', text_de_afisat_f, lista)
            firma_aleasa = lista[0]
            while firma_aleasa not in lista_firme:
                lista = []
                display_window('input', text_de_afisat_f, lista)
                firma_aleasa = lista[0]
            lista = []
            lista_tipuri1 = []
            lista_tipuri = "Alegeti un tip de produs din cele de mai jos:\n"
            exp.execute("SELECT nume_tip_produs from tip_produs")
            for result in exp:
                lista_tipuri1.append(result[0].lower())
                lista_tipuri += str(result[0]) + '\n'
            lista_tipuri += 'Tip de produs ales:'
            display_window('input', lista_tipuri, lista)
            tip_produs_ales = lista[0].lower()
            while tip_produs_ales not in lista_tipuri1:
                lista = []
                display_window('input', lista_tipuri, lista)
                tip_produs_ales = lista[0].lower()
            lista = []
            text1 = "Alegeti o stare de produs din cele de mai jos:\n"
            lista_stari = []
            exp.execute("SELECT nume_stare from stare_produs")
            for result in exp:
                text1 += str(result[0]) + '\n'
                lista_stari.append(result[0])
            text1 += 'Stare aleasa:'
            display_window('input', text1, lista)
            stare_aleasa = lista[0].lower()
            while stare_aleasa not in lista_stari:
                lista = []
                display_window('input', text1, lista)
                stare_aleasa = lista[0].lower()
            # De cautat produsul in produse
            exp.execute("(SELECT ID_P_CR FROM PRODUSE,TIP_PRODUS,stare_produs,nume_producator WHERE PRODUSE.TIP_PRODUS_ID_PRODUS=TIP_PRODUS.ID_PRODUS AND NUME_TIP_PRODUS LIKE \'" + tip_produs_ales + "\' and produse.nume_producator_id_firma=nume_producator.id_firma and nume_firma=\'" + firma_aleasa + "\' and produse.stare_produs_id_stare=stare_produs.id_stare and nume_stare=\'" + stare_aleasa + "\' and produse.car_p=\'" + caracteristica + "\' )")
            for result in exp:
                exp1=con.cursor()
                lista = []
                display_window('input', "Cantitatea vanzarii de modificat:", lista)
                cantitate_de_modificat = lista[0]
                lista = []
                display_window('input', 'Data vanzarii pentru produsul cu id-ul ' + str(
                    result[0]) + ' de modificat(format:DD-MMM-YY):', lista)
                data_de_modificat = lista[0]
                lista = []
                display_window('input', "Data dorita noua (format:DD-MMM-YY):", lista)
                data_noua = lista[0]
                lista = []
                display_window('input', "Noua cantitate dorita:", lista)
                cantitate_dorita_noua = lista[0]
                if data_noua=='':
                    data_noua=data_de_modificat
                if cantitate_dorita_noua=='':
                    cantitate_dorita_noua=cantitate_de_modificat
                try:
                    exp1.execute("BEGIN UPDATE VANZARI SET CANTITATE_DORITA="+cantitate_dorita_noua+",data='"+data_noua+"' WHERE produse_id_p_cr="+str(result[0])+"and CANTITATE_DORITA="+cantitate_de_modificat+"and data='"+data_de_modificat+"';UPDATE MAGAZIE SET CANTITATE_DISPONIBILA=CANTITATE_DISPONIBILA+" + str(int(cantitate_de_modificat)-int(cantitate_dorita_noua)) + " where PRODUSE_ID_P_CR=" + str(result[0]) + ";COMMIT; END;")
                except cx_Oracle.IntegrityError:
                    display_window('text', 'Cantitatea noua dorita este prea mare, se reia de la inceput', [])
            text_de_afisat = "Tabela modificata:\n"
            afisare_vanzari(text_de_afisat)
    except cx_Oracle.IntegrityError or cx_Oracle.DatabaseError:
        display_window('text', 'Datele introduse au fost incorecte, se reia de la inceput', [])
    except IndexError:
        pass
    finally:
        exp.close()
if __name__ == "__main__":
    initializare()
    while 1:
        operatie_dorita=[]
        display_window('input','Introduceti o operatie(vizualizare/adaugare/modificare/stergere/iesire):',operatie_dorita)
        if operatie_dorita!=[]:
            operatie_dorita[0]=operatie_dorita[0].lower()
            if operatie_dorita[0]=='vizualizare':
                afisare_tabela()
            elif operatie_dorita[0]=='adaugare':
                adaugare_in_tabela()
            elif operatie_dorita[0]=='modificare':
                modificare()
            elif operatie_dorita[0]=='stergere':
                stergere()
            elif operatie_dorita[0]=='iesire':
                con.close()
                exit(0)