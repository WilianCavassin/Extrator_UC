from os import name
import pandas as pd
import numpy as np
import nltk
import json
import pytz
import datetime

# Variáveis Globais
usecase_idgeral = 'uPvWijfSl0Thx'
class_idgeral = 'uHcXGwS8JX9pm'
xmi_name = 'Diagram_UserStories'

# Retorna o tamanho de um dataframe
def get_size_df(df):
    return len(df.index)

# Retorna o tamanho de uma lista
def get_size_list(lista):
    return len(lista)

# Retorna Timestamp padronizado GMT-3
def get_actual_timestamp():
    timestamp = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%dT%H:%M:%S")
    return timestamp

# Retorna os indices de elementos específicos em uma lista
def get_index_positions(list_elem, elem):
    list_index = [i for i in range(len(list_elem)) if list_elem[i] == elem]
    return list_index

# Verifica as virgulas, aspas, e se contem alguma string que esteja no padrão
# Não realiza verificacao gramatical neste passo
def validate_file(string_list):
    sentences_all = len(string_list)
    sentences_right = 0 
    sentences_wrong = 0
    type_return = 0
    string_return = ''
    list_return = []
    compose_return = []
    for item in string_list:
        if item.count(',') == 2 and item.count('"') == 2:
            list_return.append(item)
            print('Correta->')
            print(item)
            sentences_right = sentences_right + 1
        else:
            print('Errada->')
            print(item)
            sentences_wrong = sentences_wrong + 1 
    if sentences_right == 0 or sentences_all == 0 or sentences_all == sentences_wrong:
        string_return = 'Foram encontrados erros graves na validação inicial\nselecione outro arquivo.\nSentenças Corretas : {p_sentencesright}\nSentenças Erradas: {p_sentenceswrong}\nSentenças Totais: {p_sentencesall}'.format(p_sentencesright=sentences_right,p_sentenceswrong=sentences_wrong,p_sentencesall=sentences_all)
        compose_return = []
        type_return = 0
        compose_return.append(type_return)
        compose_return.append(string_return)
        compose_return.append(list_return)
        print(list_return)
        return compose_return
    elif sentences_wrong>0:
        string_return = 'Foram encontrados erros na validação inicial\nporém, algumas sentenças podem ser processadas.\nSentenças Corretas : {p_sentencesright}\nSentenças Erradas: {p_sentenceswrong}\nSentenças Totais: {p_sentencesall}'.format(p_sentencesright=sentences_right,p_sentenceswrong=sentences_wrong,p_sentencesall=sentences_all)
        compose_return = []
        type_return = 1
        compose_return.append(type_return)
        compose_return.append(string_return)
        compose_return.append(list_return)
        print(list_return)
        return compose_return
    else:
        string_return = 'Todas as sentenças foram validadas.\nSentenças Corretas : {p_sentencesright}\nSentenças Erradas: {p_sentenceswrong}\nSentenças Totais: {p_sentencesall}'.format(p_sentencesright=sentences_right,p_sentenceswrong=sentences_wrong,p_sentencesall=sentences_all)
        compose_return = []
        type_return = 2
        compose_return.append(type_return)
        compose_return.append(string_return)
        compose_return.append(list_return)
        print(list_return)
        return compose_return


def processData(string_list, file_name):
    global usecase_idgeral
    global xmi_name
    
    #Criar Primeiro DataFrame (extração) - df_alfa
    print('Lista de entrada:\n')
    print(string_list)
    df_alfa = pd.DataFrame(columns=['user_story','fonte'])
    df_alfa['user_story'] = string_list
    df_alfa['fonte'] = file_name
    df_alfa.fillna("", inplace=True)
    df_alfa.drop_duplicates(subset=['user_story'], keep='first', inplace=True)
    df_alfa.reset_index(drop=True, inplace=True)
    df_alfa.index.name = 'id_de'
    print(df_alfa)
    print('\n\n')
    
    #Criar Segundo DataFrame (tag) - df_beta
    df_beta = df_alfa.copy()
    df_beta['lista_gramatical'] = ''
    df_beta['lista_words'] = ''
    for index, row in df_beta.iterrows():
        pre_process = str(row['user_story']).replace('','').replace('``','').replace("''","").replace("”","").replace('"',"").replace("´´","").replace("’","").replace("“","")
        text = nltk.word_tokenize(pre_process)
        data = nltk.pos_tag(text)
        lista_gramatica = []
        lista_words = []
        for item in data:
            lista_gramatica.append(item[1])
            lista_words.append(item[0])
        lista_gramatica_json = json.dumps(lista_gramatica)
        lista_words_json = json.dumps(lista_words)
        df_beta.at[index,'lista_words'] = lista_words_json
        df_beta.at[index,'lista_gramatical'] = lista_gramatica_json
    
    print(df_beta)
    print('\n\n')

    #Criar Terceiro DataFrame (extract) - df_gama
    lista_ocorrencias = []
    for index, row in df_beta.iterrows():
        print('DATA')
        lista_gramatical = eval(row['lista_gramatical'])
        print(lista_gramatical)
        lista_words = eval(row['lista_words'])
        print(lista_words)
        lista_virgulas = get_index_positions(lista_words,',')
        print(lista_virgulas)
        ponto_final = get_index_positions(lista_words, '.')[0]
        print(ponto_final)
        print('\n\n')
        #first case find user
        papel = ''
        obj = ''
        razao = ''
        if len(lista_virgulas) == 2:
            #extrair papel
            temp_papel = ''
            for value in range(0,lista_virgulas[0]):
                if lista_gramatical[value].startswith('N'):
                    temp_papel = temp_papel + lista_words[value] + ' '
                papel = temp_papel
            #extrair objetivo
            flag_obj = False
            temp_obj = ''
            for value in range(lista_virgulas[0],lista_virgulas[1]):
                if flag_obj == False:
                    if lista_gramatical[value] == 'TO':
                        flag_obj = True
                else:
                    temp_obj = temp_obj + lista_words[value] + ' '
                obj = temp_obj
            #extrair objetivo
            flag_raz = False
            temp_raz = ''
            for value in range(lista_virgulas[1]+1,ponto_final):
                if flag_raz == False:
                    if lista_gramatical[value] != 'IN':
                        temp_raz = temp_raz + lista_words[value] + ' '
                        flag_raz = True
                else:
                    temp_raz = temp_raz + lista_words[value] + ' '
                razao = temp_raz
            print(papel)
            print(obj)
            print(razao)
        else:
            print('Encontrei uma struct fora de padrão.')
            papel = np.nan
            obj = np.nan
            razao = np.nan
        lista_ocorrencias.append([papel,obj,razao])
    df_gama = pd.DataFrame(lista_ocorrencias,columns=['Papel','Objetivo','Razao'])
    # Remove os casos diferentes do padrão (neste caso utiliza padrões gramaticais)
    print('Sem drop - gama:')
    print(df_gama)
    df_gama.dropna(thresh = 1, inplace=True)
    print('Com drop - gama:')
    print(df_gama)
    print('\n\n')

    #Criar quarto Dataframe (Geração de ids) - df_delta
    df_delta = df_gama.copy()
    df_delta['id_Papel'] = df_delta['Papel'].map(hash)
    df_delta['id_Papel'] = df_delta['id_Papel'].apply(lambda x: hex(x))
    df_delta['id_Objetivo'] = df_delta['Objetivo'].map(hash)
    df_delta['id_Objetivo'] = df_delta['id_Objetivo'].apply(lambda x: hex(x))
    df_delta['id_PapelObjetivo'] = df_delta[['id_Papel','id_Objetivo']].apply(lambda x: ''.join(x), axis=1)
    df_delta['id_Razao'] = df_delta['Razao'].map(hash)
    df_delta['id_Razao'] = df_delta['id_Razao'].apply(lambda x: hex(x))
    print(df_delta)
    print('\n\n')
    return(generate_xmi(df_delta))

# Monta o xmi seguindo o padrão Umbrello
def generate_xmi(df_delta):
    global usecase_idgeral
    global xmi_name
    timestamp = get_actual_timestamp()
    xmi_pt1 = '\
<?xml version="1.0" encoding="UTF-8"?>\n\
<XMI verified="false" xmi.version="1.2" timestamp="{p_timestamp}" xmlns:UML="http://schema.omg.org/spec/UML/1.4">\n\
 <XMI.header>\n\
  <XMI.documentation>\n\
   <XMI.exporter>umbrello uml modeller http://umbrello.kde.org</XMI.exporter>\n\
   <XMI.exporterVersion>1.6.18</XMI.exporterVersion>\n\
   <XMI.exporterEncoding>UnicodeUTF8</XMI.exporterEncoding>\n\
  </XMI.documentation>\n\
  <XMI.metamodel xmi.version="1.4" href="UML.xml" xmi.name="UML"/>\n\
 </XMI.header>\n\
 <XMI.content>\n'.format(p_timestamp = timestamp)

    xmi_pt2 = '  <UML:Model isSpecification="false" isAbstract="false" isLeaf="false" xmi.id="m1" isRoot="false" name="UML Model">\n\
   <UML:Namespace.ownedElement>\n\
    <UML:Stereotype visibility="public" isSpecification="false" namespace="m1" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="folder" name="folder"/>\n\
    <UML:Model visibility="public" isSpecification="false" namespace="m1" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="Logical_View" name="Logical View">\n\
     <UML:Namespace.ownedElement>\n\
      <UML:Package stereotype="folder" visibility="public" isSpecification="false" namespace="Logical_View" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="Datatypes" name="Datatypes">\n\
       <UML:Namespace.ownedElement>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="u6XhdNvR9KaCi" name="char"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uIfLZBCe6rLt8" name="int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uKPA1dpV7Lz0Y" name="float"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uKCK5S3g9xT6V" name="double"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="urlEOB0o80pTP" name="bool"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uYKQScHuszXbj" name="string"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="ul5h7hSAYVXb8" name="unsigned char"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uh3s1u66Op8zy" name="signed char"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="u2EV04clBU0b1" name="unsigned int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="u2d4KSzTrP0UE" name="signed int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="u00jedWezDA3L" name="short int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uSQsL1EqCiwdO" name="unsigned short int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uaFaMYqueg1a6" name="signed short int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uH4dLC0K7CNKc" name="long int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uklyhAi2N9Xpi" name="signed long int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="u3SAEGkSxno3R" name="unsigned long int"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uWKij4HKxypYL" name="long double"/>\n\
        <UML:DataType visibility="public" isSpecification="false" namespace="Datatypes" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="uXdIPQH7EW2Bu" name="wchar_t"/>\n\
       </UML:Namespace.ownedElement>\n\
      </UML:Package>\n\
     </UML:Namespace.ownedElement>\n\
     <XMI.extension xmi.extender="umbrello">\n\
      <diagrams resolution="96">\n\
       <diagram showopsig="1" linecolor="#ff0000" snapx="25" showattribassocs="1" snapy="25" linewidth="0" showattsig="1" textcolor="#000000" isopen="1" showpackage="1" showpubliconly="0" showstereotype="1" name="class diagram" font="Sans Serif,9,-1,0,50,0,0,0,0,0" canvasheight="0" canvaswidth="0" localid="-1" snapcsgrid="0" showgrid="0" showops="1" griddotcolor="#d3d3d3" backgroundcolor="#ffffff" usefillcolor="1" fillcolor="#ffff00" zoom="100" xmi.id="{p_classidgeral}" documentation="" showscope="1" snapgrid="0" showatts="1" type="1">\n\
        <widgets/>\n\
        <messages/>\n\
        <associations/>\n\
       </diagram>\n\
      </diagrams>\n\
     </XMI.extension>\n\
    </UML:Model>\n'.format(p_classidgeral = class_idgeral)
    xmi_pt3 ='    <UML:Model visibility="public" isSpecification="false" namespace="m1" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="Use_Case_View" name="Use Case View">\n\
     <UML:Namespace.ownedElement>\n'.format(p_xmiName = xmi_name)
    xmi_pt4 = ''

    #Acrescenta os papéis e objetivos, a razão pode derivar para um épico futuramente.
    list_actor = []
    list_case = []
    for index, row in df_delta.iterrows():
        if row['Papel'] not in list_actor:
            temp_ator = '      <UML:Actor visibility="public" isSpecification="false" namespace="Use_Case_View" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="{d_idp}" name="{d_namep}"/>\n'.format(d_idp = row['id_Papel'], d_namep = row['Papel'])
            list_actor.append(row['Papel'])
        else:    
            temp_actor = ''
        if row['Objetivo'] not in list_case:
            temp_case = '      <UML:UseCase visibility="public" isSpecification="false" namespace="Use_Case_View" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="{d_idc}" name="{d_namec}"/>\n'.format(d_idc = row['id_Objetivo'], d_namec = row['Objetivo'])
            list_case.append(row['Objetivo'])
        else:
            temp_case = ''
        xmi_pt4 = xmi_pt4 + temp_ator + temp_case
    print(list_actor)
    print(list_case)
    
    #Acescenta associations/ligações
    xmi_pt5 = ''
    list_assoc = []
    for index, row in df_delta.iterrows():
        if row['id_PapelObjetivo'] not in list_assoc:
            temp_assoc = '      <UML:Association visibility="public" isSpecification="false" namespace="Use_Case_View" xmi.id="{d_ida}" name="">\n\
           <UML:Association.connection>\n\
            <UML:AssociationEnd changeability="changeable" visibility="public" isNavigable="true" isSpecification="false" xmi.id="{d_ida_start}" type="{d_idp}" name="" aggregation="none"/>\n\
            <UML:AssociationEnd changeability="changeable" visibility="public" isNavigable="true" isSpecification="false" xmi.id="{d_ida_end}" type="{d_idc}" name="" aggregation="none"/>\n\
           </UML:Association.connection>\n\
          </UML:Association>\n'.format(d_ida = row['id_PapelObjetivo'],d_idp=row['id_Papel'], d_idc=row['id_Objetivo'],d_ida_start = 'start_'+row['id_PapelObjetivo'], d_ida_end = 'end_'+row['id_PapelObjetivo'])
            list_assoc.append(row['id_PapelObjetivo'])
        else:
            temp_assoc = ''
        xmi_pt5 = xmi_pt5 + temp_assoc
    xmi_pt5 = xmi_pt5 + '     </UML:Namespace.ownedElement>\n'

    #Posicoes Diagrama
    actor_width = 90
    actor_height = 90
    usecase_width = 130
    usecase_height = 55
    
    #gerar colunas de posicionamento
    df_delta['pos_Papel'] = ''
    df_delta['pos_Objetivo'] = ''
    for index,row in df_delta.iterrows():
        df_delta.at[index,'pos_Papel'] = [0, (index*(1.5*actor_height))]
        df_delta.at[index,'pos_Objetivo'] = [(2*actor_width), ((df_delta.at[index,'pos_Papel'][1])+(actor_height-usecase_height)/2)]
    print(df_delta)
    print('\n\n')

    canvas_height = (df_delta['pos_Papel'].iat[-1][1])+actor_height
    canvas_width = (df_delta['pos_Objetivo'].iat[-1][0])+usecase_width
    xmi_pt6 = '     <XMI.extension xmi.extender="umbrello">\n\
      <diagrams resolution="96">\n\
       <diagram showopsig="1" linecolor="#ff0000" snapx="25" showattribassocs="1" snapy="25" linewidth="0" showattsig="1" textcolor="#000000" isopen="1" showpackage="1" showpubliconly="0" showstereotype="1" name="{name}" font="Sans Serif,9,-1,0,50,0,0,0,0,0" canvasheight="{canvas_height}" canvaswidth="{canvas_width}" localid="-1" snapcsgrid="0" showgrid="0" showops="1" griddotcolor="#d3d3d3" backgroundcolor="#ffffff" usefillcolor="1" fillcolor="#ffff00" zoom="100" xmi.id="{usecase_idgeral}" documentation="" showscope="1" snapgrid="0" showatts="1" type="2">\n\
        <widgets>\n'.format(name = xmi_name, canvas_height=canvas_height, canvas_width = canvas_width, usecase_idgeral=usecase_idgeral)
    
    #Posiciona Objetos
    xmi_pt7 = ''
    list_actor2 = []
    list_case2 = []
    for index, row in df_delta.iterrows():
        if row['Papel'] not in list_actor2:
            temp_actor2 = '         <actorwidget width="{d_width_act}" showstereotype="1" x="{d_x_act}" usesdiagramusefillcolor="0" y="{d_y_act}" usesdiagramfillcolor="0" isinstance="0" localid="{d_id_pos}" fillcolor="#ffff00" height="{d_height_act}" linecolor="#ff0000" xmi.id="{d_id_act}" autoresize="1" textcolor="#000000" usefillcolor="1" linewidth="0" font="Sans Serif,9,-1,0,50,0,0,0,0,0"/>\n'.format(d_width_act = actor_width , d_x_act = row['pos_Papel'][0], d_y_act = row['pos_Papel'][1], d_id_pos = 'pos_'+row['id_Papel'], d_height_act = actor_height,d_id_act = row['id_Papel'])        
            list_actor2.append(row['Papel'])
        else:
            temp_actor2 = ''            
        if row['Objetivo'] not in list_case2:
            temp_case2 = '         <usecasewidget width="{d_width_uc}" showstereotype="1" x="{d_x_uc}" usesdiagramusefillcolor="0" y="{d_y_uc}" usesdiagramfillcolor="0" isinstance="0" localid="{d_id_pos}" fillcolor="#ffff00" height="{d_height_uc}" linecolor="#ff0000" xmi.id="{d_id_uc}" autoresize="1" textcolor="#000000" usefillcolor="1" linewidth="0" font="Sans Serif,9,-1,0,50,0,0,0,0,0"/>\n'.format(d_width_uc = usecase_width , d_x_uc = row['pos_Objetivo'][0], d_y_uc = row['pos_Objetivo'][1], d_id_pos = 'pos_'+row['id_Objetivo'], d_height_uc = usecase_height,d_id_uc = row['id_Objetivo'])
            list_case2.append(row['Objetivo'])
        else:
            temp_case2 = ''
        xmi_pt7 = xmi_pt7 + temp_actor2 + temp_case2
    xmi_pt7 = xmi_pt7 + '        </widgets>\n\
        <messages/>\n\
        <associations>\n'

    #Posiciona Associations
    xmi_pt8 = ''
    for index,row in df_delta.iterrows():
        temp_assoc2 = '         <assocwidget indexa="1" linecolor="#ff0000" usesdiagramfillcolor="1" widgetbid="{p_idobjetivo}" indexb="1" linewidth="0" seqnum="" textcolor="none" usesdiagramusefillcolor="1" totalcounta="2" totalcountb="2" widgetaid="{p_widgetaid}" font="Sans Serif,9,-1,0,50,0,0,0,0,0" localid="{p_localid}" usefillcolor="1" fillcolor="none" xmi.id="{p_xmiid}" autoresize="1" type="503">\n\
          <linepath layout="Direct">\n\
           <startpoint startx="{p_startx}" starty="{p_starty}"/>\n\
           <endpoint endx="{p_endx}" endy="{p_endy}"/>\n\
          </linepath>\n\
         </assocwidget>\n'.format(p_idobjetivo=row['id_Objetivo'],p_widgetaid=row['id_Papel'],p_localid='pos_'+row['id_PapelObjetivo'],p_xmiid=row['id_PapelObjetivo'],p_startx=int(actor_width),p_starty=int((row['pos_Papel'][1])+actor_height/3),p_endx=int(3*actor_width),p_endy=int(row['pos_Objetivo'][1]+(actor_height/3)))
        xmi_pt8 = xmi_pt8 + temp_assoc2
    xmi_pt8 = xmi_pt8 + '        </associations>\n\
       </diagram>\n\
      </diagrams>\n\
     </XMI.extension>\n\
    </UML:Model>\n\
    <UML:Model visibility="public" isSpecification="false" namespace="m1" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="Component_View" name="Component View">\n\
     <UML:Namespace.ownedElement/>\n\
    </UML:Model>\n\
    <UML:Model visibility="public" isSpecification="false" namespace="m1" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="Deployment_View" name="Deployment View">\n\
     <UML:Namespace.ownedElement/>\n\
    </UML:Model>\n\
    <UML:Model visibility="public" isSpecification="false" namespace="m1" isAbstract="false" isLeaf="false" isRoot="false" xmi.id="Entity_Relationship_Model" name="Entity Relationship Model">\n\
     <UML:Namespace.ownedElement/>\n\
    </UML:Model>\n\
   </UML:Namespace.ownedElement>\n\
  </UML:Model>\n\
 </XMI.content>\n'
    
    #Posiciona os objetos inerentes
    xmi_pt9 = ' <XMI.extensions xmi.extender="umbrello">\n\
  <docsettings viewid="{usecase_idgeral}" uniqueid="ukUg5dcbieGSj" documentation=""/>\n\
  <listview>\n'.format(usecase_idgeral = usecase_idgeral)
    xmi_pt10 ='   <listitem open="1" type="800" id="Views">\n\
    <listitem open="1" type="821" id="Component_View"/>\n\
    <listitem open="1" type="827" id="Deployment_View"/>\n\
    <listitem open="1" type="836" id="Entity_Relationship_Model"/>\n\
    <listitem open="1" type="801" id="Logical_View">\n\
     <listitem open="0" type="807" id="{class_idgeral}" label="class diagram"/>\n\
     <listitem open="0" type="830" id="Datatypes">\n\
      <listitem open="1" type="829" id="uAVd5abE7ZApe"/>\n\
      <listitem open="0" type="829" id="uxFXJICE4GUKB"/>\n\
      <listitem open="0" type="829" id="uijpA8VDW3Pv7"/>\n\
      <listitem open="1" type="829" id="uD4bxmBJAZ7hx"/>\n\
      <listitem open="0" type="829" id="uWreomcv0M5GK"/>\n\
      <listitem open="0" type="829" id="uomR2LlW8DozS"/>\n\
      <listitem open="0" type="829" id="ujRNawgVIGPZu"/>\n\
      <listitem open="1" type="829" id="uDrwMUegB1Eli"/>\n\
      <listitem open="1" type="829" id="uxYjw1BROAiTd"/>\n\
      <listitem open="0" type="829" id="ubxQzZosJhIV8"/>\n\
      <listitem open="0" type="829" id="ucc6esQ00TxHN"/>\n\
      <listitem open="1" type="829" id="uQ7llbmbLfOM1"/>\n\
      <listitem open="1" type="829" id="u7C5Lz7tdaERg"/>\n\
      <listitem open="0" type="829" id="upge93jPREmr7"/>\n\
      <listitem open="0" type="829" id="ucteracM5INNs"/>\n\
      <listitem open="0" type="829" id="ui8Pv5oz8puo1"/>\n\
      <listitem open="0" type="829" id="uNqHZrYOhMYtG"/>\n\
      <listitem open="0" type="829" id="uZOm0aHIkv66C"/>\n\
      <listitem open="0" type="829" id="uXC09nTaRYyJy"/>\n\
      <listitem open="1" type="829" id="u22QKrKpVGgTK"/>\n\
      <listitem open="0" type="829" id="uEG94YALUp6VF"/>\n\
      <listitem open="0" type="829" id="uQlIgPihBvasc"/>\n\
      <listitem open="0" type="829" id="uCrXwEcX9P48t"/>\n\
      <listitem open="0" type="829" id="uCbAkvejkQm2W"/>\n\
      <listitem open="0" type="829" id="uns4xmfxkzRBk"/>\n\
     </listitem>\n\
    </listitem>\n'.format(class_idgeral = class_idgeral)
    xmi_pt11 = '    <listitem open="1" type="802" id="Use_Case_View">\n'
    for index,row in df_delta.iterrows():
        temp_case3 = '     <listitem open="1" type="812" id="{b01}"/>\n'.format(b01 = row['id_Objetivo'])
        temp_actor3 = '     <listitem open="1" type="811" id="{b02}"/>\n'.format(b02 = row['id_Papel'])
        xmi_pt11 = xmi_pt11 + temp_case3 + temp_actor3
    print(xmi_pt11)
    xmi_pt12 ='     <listitem open="1" type="805" id="{usecase_idgeral}" label="{xmi_name}"/>\n\
    </listitem>\n\
   </listitem>\n\
  </listview>\n\
  <codegeneration>\n\
   <codegenerator language="Python"/>\n\
  </codegeneration>\n\
 </XMI.extensions>\n\
</XMI>'.format(usecase_idgeral = usecase_idgeral, xmi_name = xmi_name)
    xmi_full = xmi_pt1+xmi_pt2+xmi_pt3+xmi_pt4+xmi_pt5+xmi_pt6+xmi_pt7+xmi_pt8+xmi_pt9+xmi_pt10+xmi_pt11+xmi_pt12
    print(xmi_full)
    return xmi_full