from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from io import StringIO
import psycopg2
import pandas as pd
import numpy as np
from os.path import exists
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from inventory_stock.models import MaterialSheet
import dask.dataframe as dd
# Create your views here.
def upload_files(request):
    #get current year and week
    year=datetime.datetime.today().isocalendar()[0]
    week=datetime.datetime.today().isocalendar()[1]
    conn = psycopg2.connect(host='localhost',dbname='latecoere',user='postgres',password='054Ibiza',port='5432')
    # material_sheet_file=r"\\centaure\Extract_SAP\SQ00-FICHE_ARTICLE\IS_FICHE_ARTICLE_"+format(year)+format(week)+".xlsx"
    # zpp_flg13_file=r"\\centaure\Extract_SAP\10-ZPP_FLG13\Z13_"+format(year)+format(week)+"_2.TXT"
    # mb52_file=r"\\centaure\Extract_SAP\MB52\MB52_"+format(year)+format(week)+".xlsx"
    # t001_file= r"\\centaure\Extract_SAP\SE16N-T001\T001_"+format(year)+format(week)+".xlsx"
    # t001k_file= r"\\centaure\Extract_SAP\SE16N-T001K\T001K_"+format(year)+format(week)+".XLSX "
    # tcurr_file= r"\\centaure\Extract_SAP\SE16N-TCURR\TCURR_"+format(year)+format(week)+".XLSX"

    material_sheet_file=r"\\prfoufiler01\donnees$\Public\Input_inventory_stock\IS_FICHE_ARTICLE_202236.XLSX"
    zpp_flg13_file=r"\\prfoufiler01\donnees$\Public\Input_inventory_stock\ZFLG13.TXT"
    mb52_file=r"\\prfoufiler01\donnees$\Public\Input_inventory_stock\MB52_202235.XLSX"
    t001_file= r"\\prfoufiler01\donnees$\Public\Input_inventory_stock\T001_202236.XLSX"
    t001k_file= r"\\prfoufiler01\donnees$\Public\Input_inventory_stock\T001K_202236.XLSX"
    tcurr_file= r"\\prfoufiler01\donnees$\Public\Input_inventory_stock\TCURR_202236.XLSX"
    
    material_sheet_file_exists=exists(material_sheet_file)
    zpp_flg13_file_exists=exists(zpp_flg13_file)
    mb52_file_exists=exists(mb52_file)
    t001_file_exists=exists(t001_file)
    t001k_file_exists=exists(t001k_file)
    tcurr_file_exists=exists(tcurr_file)

    message_error= ''
    if material_sheet_file_exists == False:
        message_error= 'Unable to upload SQ00-FICHE_ARTICLE File, not exist or unreadable!'
        return render(request,'inventory_stock\index.html',{'message_error':message_error})  
    if zpp_flg13_file_exists == False:
        zpp_flg13_file=r"\\centaure\Extract_SAP\10-ZPP_FLG13\Z13_"+format(year)+format(week)+"_1.TXT"
        zpp_flg13_file_1_exists = exists(zpp_flg13_file)
        if zpp_flg13_file_1_exists == False:
            message_error= 'Unable to upload ZPP FLG13 File, not exist or unreadable!'
            return render(request,'inventory_stock\index.html',{'message_error':message_error}) 
    if mb52_file_exists == False:
        message_error= 'Unable to upload MB52 File, not exist or unreadable!'
        return render(request,'inventory_stock\index.html',{'message_error':message_error})         
    if t001_file_exists == False:
        message_error= 'Unable to upload TOO1 File, not exist or unreadable!'
        return render(request,'inventory_stock\index.html',{'message_error':message_error})   
    if t001k_file_exists == False:
        message_error= 'Unable to upload TK001 File, not exist or unreadable!'
        return render(request,'inventory_stock\index.html',{'message_error':message_error}) 
    if tcurr_file_exists == False:
        message_error= 'Unable to upload TCURR File, not exist or unreadable!'
        return render(request,'inventory_stock\index.html',{'message_error':message_error}) 
    
    import_files(material_sheet_file,zpp_flg13_file,mb52_file,t001_file,t001k_file,tcurr_file,year,week,conn)
    return home(request)


def home(request):
    current_week=datetime.datetime.now().isocalendar().week
    current_year=datetime.datetime.now().isocalendar().year
    username=request.META['REMOTE_USER']
    all_MaterialSheet_data= MaterialSheet.objects.all()
    weekavailable=all_MaterialSheet_data.values_list('week',flat=True).distinct().order_by('week') #flat=True will remove the tuples and return the list   
    yearavailable=all_MaterialSheet_data.values_list('year',flat=True).distinct().order_by('year') #flat=True will remove the tuples and return the list   
    division=[]
    profit_center=[]
    week=[]
    year=[]
    if request.method=='POST':
        division=request.POST.getlist('division')
        week=request.POST.getlist('week')
        year=request.POST.getlist('year')
        profit_center=request.POST.getlist('profit_center')
    
    message_error=''
    if len(year) > 0:
        MaterialSheet_data=all_MaterialSheet_data.filter(year__in=year)
        if len(week) > 0:
            MaterialSheet_data=all_MaterialSheet_data.filter(year__in=year,week__in=week)
            if len(division) > 0:
                MaterialSheet_data=MaterialSheet_data.filter(division__in=division)
            if len(profit_center) > 0:
                MaterialSheet_data=MaterialSheet_data.filter(profit_center__in=profit_center)
    else:
        MaterialSheet_data=all_MaterialSheet_data.filter(week=current_week,year=current_year)

    if MaterialSheet_data:
        inventory_stock_results(MaterialSheet_data)
    else:
        message_error='There is no data with your selected filter'
        inventory_stock_results.total_count=None
        inventory_stock_results.total_pmp_unit_euro=None
        inventory_stock_results.total_ps_unit_euro_cost=None
        inventory_stock_results.total_valuation_ps_euro_cost=None
        inventory_stock_results.total_valuation_pmp_euro_cost=None
        inventory_stock_results.division_pmp_unit_euro=None
        inventory_stock_results.division_ps_unit_euro_cost=None
        inventory_stock_results.division_valuation_ps_euro_cost=None
        inventory_stock_results.division_valuation_pmp_euro_cost=None


    return render(request,'inventory_stock\index.html',{
    'username':username,'current_week':current_week,'profit_center':profit_center,
    'weekavailable':weekavailable,'yearavailable':yearavailable,'message_error':message_error,'weeks':week,'years':year,'divisions':division,
    'inventory_stock_results_total_count':inventory_stock_results.total_count,
    'inventory_stock_results_total_pmp_unit_euro':inventory_stock_results.total_pmp_unit_euro,
    'inventory_stock_results_total_ps_unit_euro_cost':inventory_stock_results.total_ps_unit_euro_cost,
    'inventory_stock_results_total_valuation_ps_euro_cost':inventory_stock_results.total_valuation_ps_euro_cost,
    'inventory_stock_results_total_valuation_pmp_euro_cost':inventory_stock_results.total_valuation_pmp_euro_cost,
    'inventory_stock_results_division_pmp_unit_euro':inventory_stock_results.division_pmp_unit_euro,
    'inventory_stock_results_division_ps_unit_euro_cost':inventory_stock_results.division_ps_unit_euro_cost,
    'inventory_stock_results_division_valuation_ps_euro_cost':inventory_stock_results.division_valuation_ps_euro_cost,
    'inventory_stock_results_division_valuation_pmp_euro_cost':inventory_stock_results.division_valuation_pmp_euro_cost,
    })

def inventory_stock_results(MaterialSheet_data):
    df=pd.DataFrame(MaterialSheet_data.values())
    inventory_stock_results.total_count=df.shape[0]
    inventory_stock_results.total_pmp_unit_euro=df['pmp_unit_euro'].sum()
    inventory_stock_results.total_ps_unit_euro_cost=df['ps_unit_euro'].sum()
    inventory_stock_results.total_valuation_ps_euro_cost=df['valuation_ps_euro'].sum()
    inventory_stock_results.total_valuation_pmp_euro_cost=df['valuation_pmp_euro'].sum()

    inventory_stock_results.division_pmp_unit_euro=df.groupby(['division'])['pmp_unit_euro'].sum().reset_index()
    inventory_stock_results.division_ps_unit_euro_cost=df.groupby(['division'])['ps_unit_euro'].sum().reset_index()
    inventory_stock_results.division_valuation_ps_euro_cost=df.groupby(['division'])['valuation_ps_euro'].sum().reset_index()
    inventory_stock_results.division_valuation_pmp_euro_cost=df.groupby(['division'])['valuation_pmp_euro'].sum().reset_index()

    


def details(request):
    data=pd.DataFrame(MaterialSheet.objects.all().values())
    message_success=''

    now = datetime.datetime.now()
    current_time = now.strftime("%d_%m_%y_%H:%M:%S")

    # Convert dataframe to dic for paginitation
    records = data.to_dict(orient='records')

    paginator = Paginator(records, 50)
    page = request.GET.get('page')
    records = paginator.get_page(page)
    if request.method == 'POST':
        # Download file 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=inventory_stock_details_'+current_time+'.csv'
        # data.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")
        data.to_csv(path_or_buf=response,index=False)
        return response
    return render(request,"inventory_stock/details.html",{'data':records,'message_success':message_success})

def import_files(material_sheet_file,zpp_flg13_file,mb52_file,t001_file,t001k_file,tcurr_file,year,week,conn):
    print('Hello')
    df=pd.read_excel(material_sheet_file)
    print('End df')
    df_mb52=pd.read_excel(mb52_file)
    print('End df_mb52')
    df_t001=pd.read_excel(t001_file)
    print('End df_t001')
    df_t001k=pd.read_excel(t001k_file)
    print('End df_t001k')
    df_tcurr=pd.read_excel(tcurr_file)
    print('End df_tcurr')
    df_zpp_flg13=dd.read_csv(zpp_flg13_file,encoding='ANSI',sep=';',dtype={'Division': 'object','Gestionnaire':'object','Type article':'object'})
    print('End ZPP FLG13')



    df_t001k = df_t001k.iloc[:, [0,1]]
    df_t001k.rename(columns={'Domaine valorisation':'division','Société':'company'},  inplace = True)

    df_t001=df_t001.iloc[:, [0,4]]
    df_t001.rename(columns={'Société':'company','Devise':'currency'},  inplace = True)

    df_tcurr=df_tcurr[ ( df_tcurr['Type de cours'].isin(['M','P']) ) & (df_tcurr['Dev. source']=='EUR') ]
    df_tcurr=df_tcurr.iloc[:, [2,3,4]]
    df_tcurr.rename(columns={'Devise cible':'target_currency','Début validité':'date','Taux':'rate'},  inplace = True)
    df_tcurr['date']=pd.to_datetime( df_tcurr['date'])
    df_tcurr=df_tcurr.sort_values(['target_currency', 'date'],ascending = [True, False])
    df_tcurr=df_tcurr.groupby(['target_currency'])['rate'].first().reset_index() 

    #I use Période and Grp acheteurs instead Division and Material 
    # because can't read proprely the file with dask ther's an offset between headers and data
    df_zpp_flg13['key']=df_zpp_flg13['Période'].astype('str')+df_zpp_flg13['Grp acheteurs'].astype('str')
    dict_zpp_flg13_stock=dict(zip(df_zpp_flg13['key'],df_zpp_flg13['Stock']))
    dict_zpp_flg13_lot_qm=dict(zip(df_zpp_flg13['key'],df_zpp_flg13['Lot QM']))
    dict_zpp_flg13_stock_transit=dict(zip(df_zpp_flg13['key'],df_zpp_flg13['Stock en Transit']))


    df=df.iloc[:,[0,1,4,6,26,62,63,88]]
    df.rename(columns={'Article':'material','Division':'division','TypArt':'material_type','I/C':'individual_collective','Prix standard':'standard_price','Base de prix':'price_basis','Pr.moy.pond':'pr_moy_pond'},  inplace = True)
    df["division"]=df["division"].fillna(0).astype(int)
    df.insert(0, 'year', year)
    df.insert(1, 'week', week)

    df=df[ ( df['material_type'].isin(['AF','CA']) ) & (df['individual_collective'] == 2.0 ) ]
    # Merge files
    # Get company from t0001k
    df_t001k_dict=dict(zip(df_t001k['division'],df_t001k['company']))
    df['company']=df['division'].map(df_t001k_dict)
    # Get currency from t001
    df_t001_dict=dict(zip(df_t001['company'],df_t001['currency']))
    df['currency']=df['company'].map(df_t001_dict)
    # Get rate  from tcurr
    df_tcurr_dict=dict(zip(df_tcurr['target_currency'],df_tcurr['rate']))
    df['rate']=df['currency'].map(df_tcurr_dict)
    df['rate'] = df['rate'].str.replace(',','.')
    df['rate']=df['rate'].fillna(1)
    df['rate']=df['rate'].astype(float)

    df['ps_unit_div']=np.where((df['rate'] == 'TND'), (df['standard_price'] / df['price_basis'])*10 , (df['standard_price'] / df['price_basis']))
    df['pmp_unit_div']=np.where((df['rate'] == 'TND'), (df['pr_moy_pond'] / df['price_basis'])*10 , (df['pr_moy_pond'] / df['price_basis']))

    df['ps_unit_euro']=np.where( (df['currency'] == 'EUR') , df['standard_price'] , (df['standard_price'] / df['price_basis'] / df['rate']) )
    df['pmp_unit_euro']=np.where( (df['currency'] == 'EUR') , df['pr_moy_pond'] , (df['pr_moy_pond'] / df['price_basis'] / df['rate']) )

    df['key']=df['division'].astype('str')+df['material'].astype('str')

    df['stock']=df['key'].map(dict_zpp_flg13_stock)
    df['lot_qm']=df['key'].map(dict_zpp_flg13_lot_qm)
    df['stock_transit']=df['key'].map(dict_zpp_flg13_stock_transit)

    df_mb52['key']=df_mb52['Division'].astype('str')+df_mb52["Numéro d'article"].astype('str')
    dict_df_mb52_stock_blocked=dict(zip(df_mb52['key'],df_mb52['Bloqué']))
    df['stock_bloqued']=df['key'].map(dict_df_mb52_stock_blocked)

    df['valuation_ps_div']=(df['stock']+df['lot_qm']+df['stock_transit']+df['stock_bloqued']) * df['ps_unit_div']
    df['valuation_pmp_div']=(df['stock']+df['lot_qm']+df['stock_transit']+df['stock_bloqued']) * df['pmp_unit_div']
    df['valuation_ps_euro']=(df['stock']+df['lot_qm']+df['stock_transit']+df['stock_bloqued']) * df['ps_unit_euro']
    df['valuation_pmp_euro']=(df['stock']+df['lot_qm']+df['stock_transit']+df['stock_bloqued']) * df['pmp_unit_euro']
    
    del df['key']
    # df.to_csv('df_inventroy_stock.csv')
    # print(df)
    data = StringIO()
    #convert file to csv
    data.write(df.to_csv( header=None, index=False ,sep=';'))
    # This will make the cursor at index 0
    data.seek(0)
    with conn.cursor() as c:
        c.copy_from(
            file=data,
            #file name in DB
            table="inventory_stock_materialsheet",
            columns=[
                'year',
                'week',
                'material',
                'division',
                'profit_center',
                'material_type',
                'individual_collective',
                'standard_price',
                'pr_moy_pond',
                'price_basis', 
                'company',
                'currency', 
                'rate', 
                'ps_unit_div',
                'pmp_unit_div',
                'ps_unit_euro',
                'pmp_unit_euro',
                'stock',
                'lot_qm',
                'stock_transit',
                'stock_blocked',
                'valuation_ps_div',
                'valuation_pmp_div',
                'valuation_ps_euro',
                'valuation_pmp_euro',   
            ],
            null="",
            sep=";",
        )

    conn.commit()
    

