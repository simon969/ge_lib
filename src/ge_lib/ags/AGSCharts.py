import io
# from .AGS4_fs import AGS4_to_dataframe
from python_ags4.AGS4 import AGS4_to_dataframe
import matplotlib.colors as mcolors
from rich import print as rprint

from .AGSData import get_df, get_group_by

color_names = list(mcolors.cnames.keys())

charted_groups = {'groups': ['core', 'dcpt', 'dcpg', 'eres', 'gchm', 'ispt', 'lden', 'llpl', 'lnmc', 'lvan', 'mond', 'rden', 'trit', 'wstd'],
                  'layouts': ['2up','a4 landscape', 'group'],
                  'formats': ['jpg','pdf','png','svg']
                  }
supported_formats = ['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'tif', 'tiff', 'webp']

def get_data_chart (input_file, tables, table, formats, layouts, errors):
    
    if table == 'core':
        return chart_core (input_file, tables, formats, layouts, errors)
    if table == 'dcpt':
        return chart_dcpt (input_file, tables, formats, layouts, errors)   
    if table == 'dcpg':
        return chart_dcpg (input_file, tables, formats, layouts, errors)   
    if table == 'eres':
        return chart_eres (input_file, tables, formats, layouts, errors) 
    if table == 'gchm':
        return chart_gchm (input_file, tables, formats, layouts, errors)   
    if table == 'ispt':
        return chart_ispt (input_file, tables, formats, layouts, errors)
    if table == 'llpl':
        return chart_llpl (input_file, tables, formats, layouts, errors)      
    if table == 'lden':
        return chart_lden (input_file, tables, formats, layouts, errors)      
    if table == 'lnmc':
        return chart_lnmc (input_file, tables, formats, layouts, errors)      
    if table == 'lvan':
        return chart_lvan (input_file, tables, formats, layouts, errors)
    if table == 'mond':
        return chart_mond (input_file, tables, formats, layouts, errors) 
    if table == 'rden':
        return chart_rden (input_file, tables, formats, layouts, errors)  
    if table == 'trit':
        return chart_trit (input_file, tables, formats, layouts, errors)
    if table == 'wstd':
        return chart_wstd (input_file, tables, formats, layouts, errors)  
    return None, None

def get_units_unit(df, field):
    unit = ''
    units = df.query("HEADING == 'UNIT'")
    unit = str(units[field].iloc[0])   
    return unit

def get_units_mond(df, field):
    unit = ''
    data = df.loc[(df['HEADING']=='DATA')]
    if len(data.index)>0:
        unit = data['MOND_UNIT'].iloc[0]
    return unit

def get_units_eres(df, field):
    unit = ''
    data = df.loc[(df['HEADING']=='DATA')]
    if len(data.index)>0:    
        unit = data['ERES_RUNI'].iloc[0]
    return unit

def get_units_gchm(df, field):
    unit = '' 
    data = df.loc[(df['HEADING']=='DATA')]
    if len(data.index)>0:
        unit = data['GCHM_UNIT'].iloc[0]
    return unit

def get_value_names(df, x_fields):
    return "-".join(x_fields)

def get_value_name_eres(df, fields):
    name = ''
    data = df.loc[(df['HEADING']=='DATA')]
    if len(data.index)>0:
        name = data['ERES_NAME'].iloc[0]
    return name

def get_value_name_mond(df, fields):
    name = ''
    data = df.loc[(df['HEADING']=='DATA')]
    if len(data.index)>0:
        name = data['MOND_TYPE'].iloc[0]
    return name

def get_value_name_gchm(df, fields):
    name = ''
    data = df.loc[(df['HEADING']=='DATA')]
    if len(data.index) > 0:
        name = data['GCHM_CODE'].iloc[0]
    return name

page_sizes = {'a7 portrait':  {'x':2.9, 'y':4.1},
              'a7 landscape': {'x':4.1, 'y':2.9},
              'a6 portrait':  {'x':4.1, 'y':5.8},
              'a6 landscape': {'x':5.8, 'y':4.1},
              'a5 portrait':  {'x':5.8, 'y':8.3},
              'a5 landscape': {'x':8.3, 'y':5.8},
              'a4 portrait':  {'x':8.3, 'y':11.7},
              'a4 landscape': {'x':11.7, 'y':8.3},
              'a3 portrait':  {'x':11.7, 'y':16.5},
              'a3 landscape': {'x':16.5, 'y':11.7}
              }

def get_page_size(layouts, not_found):
    for lo in layouts:
        if lo in page_sizes:
            return page_sizes[lo]
    return not_found

def get_supported_formats(try_formats, accept_formats):
    formats = []
    for f in try_formats:
        if f in accept_formats:
            formats.append(f)
    return formats

def get_chart_grouped (df,
                        table, 
                        x_fields = [],
                        y_fields = ['depth','level'],
                        get_units = get_units_unit,
                        get_value_name = get_value_names,
                        group_by = ['LOCA_ID','GEOL_GEOL','GEOL_GEO2','GEOL_GEO3','GEOL_LEG'],
                        formats = ['png','jpg','pdf'],
                        layouts = ['1up','2up','xaxis_datetime','a4 portrait','a4 landscape','a3 portrait','a3 landscape'],
                        errors = []):
        
    import matplotlib
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    
    matplotlib.use('agg')

    plots = []
    names = []
    color_start = 10

    if df is None:
        return plots, names
    
    ps = get_page_size(layouts,'a4 landscape')
    formats = get_supported_formats (formats, supported_formats)

    unit = get_units(df,x_fields[0])
    groups =  get_group_by(df.query("HEADING == 'DATA'"), x_fields, group_by)

    for x_val in x_fields:
       
        for group in groups:
                
                if '2up' in layouts and len(y_fields) == 2:
                    fig, (a0, a1) = plt.subplots(1, 2, figsize=(ps['x'], ps['y']))  
                    a0.invert_yaxis()
                    color_index = color_start 
                    x_name = get_value_name(df, [x_val])
                    xlabel = x_name + ' (' + str(unit) + ')'
                    for key, grp in df.query("HEADING == 'DATA'").groupby(group):
                        grp.plot(kind="scatter", ax=a0, x=x_val, y=y_fields[0], label=key, c=color_names[color_index])
                        grp.plot(kind="scatter", ax=a1, x=x_val, y=y_fields[1], label=key, c=color_names[color_index])
                        color_index += 1
                    a0.set_xlabel(xlabel)
                    a1.set_xlabel(xlabel)
                    a0.grid(visible=True,which='both')
                    a1.grid(visible=True,which='both')
                   
                    for f in formats: 
                        image = io.BytesIO()
                        fig.savefig(image, format=f)
                        s = f'{table}_{x_name}_by_{group}.{f}'
                        names.append (s)
                        plots.append (image.getvalue())
                    plt.close(fig)

                if '1up' in layouts:
                    for y_val in y_fields:
                        fig, (a0) = plt.subplots(figsize=(ps['x'], ps['y']))  
                        if y_val=='depth':
                            a0.invert_yaxis()
                        color_index = color_start 
                        x_name = get_value_name(df, [x_val]) 
                        xlabel = x_name + ' (' + str(unit) + ')'
                        for key, grp in df.query("HEADING == 'DATA'").groupby(group):
                            grp.plot(kind="scatter", ax=a0, x=x_val, y=y_val, label=key, c=color_names[color_index])
                            color_index += 1
                        a0.set_xlabel(xlabel)
                        a0.grid(visible=True,which='both')
                        for f in formats: 
                            image = io.BytesIO()
                            fig.savefig(image, format=f)
                            s = f'{table}_{x_name}_by_{group}_{y_val}.{f}'
                            names.append (s)
                            plots.append (image.getvalue())
                        plt.close(fig)
            
                if 'xaxis_datetime' in layouts: 
                    unit = get_units(df,y_fields[0])
                    y_name  = get_value_name(df,y_fields)
                    ylabel = y_name + ' (' + unit + ')'   
                    fig, (a0) = plt.subplots(figsize=(ps['x'], ps['y']))   
                    a0.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                    a0.xaxis.set_major_locator(mdates.DayLocator(interval=5))
                    for y_val in y_fields:   
                        color_index = color_start
                        for key, grp in df.query("HEADING == 'DATA'").groupby(group):
                            grp.plot(kind="scatter", ax=a0, x=x_val, y=y_val, label=key, c=color_names[color_index])
                            color_index += 1
                        a0.set_xlabel ('Reading datetime')
                        a0.set_ylabel(ylabel) 
                        a0.grid(visible=True,which='both')
                        fig.autofmt_xdate()
                        for f in formats: 
                            image = io.BytesIO()
                            fig.savefig(image, format=f)
                            s = f'{table}_{y_name}_by_{group}_by_datetime.{f}'
                            names.append (s)
                            plots.append (image.getvalue())
                        plt.close(fig)

    return plots, names

def get_chart (df,
                table, 
                x_fields = [],
                y_fields = ['depth','level'], 
                get_units = get_units_unit,
                get_value_name = get_value_names,
                formats = ['png','jpg','pdf'],
                layouts = ['1up','2up','xaxis_datetime','a4 portrait','a4 landscape','a3 portrait','a3 landscape'],
                errors = []):
        
    import matplotlib
    import matplotlib.pyplot as plt
    
    matplotlib.use('agg')

    plots = []
    names = []
    color_start = 10

    if df is None:
        return plots, names
    
    ps = get_page_size(layouts,'a4 landscape')
    formats = get_supported_formats (formats, supported_formats)

    if '2up' in layouts and len(y_fields) == 2:
        unit = get_units (df,x_fields[0])
        x_name  = get_value_name(df, x_fields)
        fig, (a0, a1) = plt.subplots(1, 2, figsize=(ps['x'], ps['y']))  
        a0.invert_yaxis()
        color_index = color_start 
        xlabel = x_name + ' (' + unit + ')'
        for x_val in x_fields:
            df.query("HEADING == 'DATA'").plot(kind="scatter", ax=a0, x=x_val, y=y_fields[0], label=x_val, c=color_names[color_index])
            df.query("HEADING == 'DATA'").plot(kind="scatter", ax=a1, x=x_val, y=y_fields[1], label=x_val, c=color_names[color_index])
            color_index += 1
        a0.set_xlabel(xlabel)
        a1.set_xlabel(xlabel)
        a0.grid(visible=True,which='both')
        a1.grid(visible=True,which='both')
        for f in formats: 
            image = io.BytesIO()
            fig.savefig(image, format=f)
            s = f'{table}_{x_name}.{f}'
            names.append (s)
            plots.append (image.getvalue())
        plt.close(fig)

    if '1up' in layouts:
        unit = get_units (df,x_fields[0])
        x_name  = get_value_name(df, x_fields)
        for y_val in y_fields: 
            fig, (a0) = plt.subplots(figsize=(ps['x'], ps['y']))  
            if y_val=='depth':
                a0.invert_yaxis()
            xlabel = x_name + ' (' + unit + ')'   
            for x_val in x_fields:
                color_index = color_start
                df.plot(kind="scatter", ax=a0, x=x_val, y=y_val, c=color_names[color_index])
                color_index += 1
            a0.grid(visible=True,which='both')
            a0.set_xlabel(xlabel)
            for f in formats: 
                image = io.BytesIO()
                fig.savefig(image, format=f)
                s = f'{table}_{x_name}_{y_val}.{f}'
                names.append (s)
                plots.append (image.getvalue())
            plt.close(fig)
    
    if 'xaxis_datetime' in layouts:
        unit = get_units (df, y_fields[0])
        y_name  = get_value_name(df, y_fields)
        for x_val in x_fields: 
            fig, (a0) = plt.subplots(figsize=(ps['x'], ps['y'])) 
            y_label = y_name + ' (' + unit + ')'   
            for y_val in y_fields:
                color_index = color_start
                df.plot(kind="scatter", ax=a0, x=x_val, y=y_val, c=color_names[color_index])
                color_index += 1
            a0.grid(visible=True, which='both')
            a0.set_ylabel(y_label)
            a0.set_xlabel ('Reading datetime')
            for f in formats: 
                image = io.BytesIO()
                fig.savefig(image, format=f)
                s = f'{table}_{y_name}_by_datetime.{f}'
                names.append (s)
                plots.append (image.getvalue())
            plt.close(fig)
    
    return plots, names

def bar_chart():

    # data from https://allisonhorst.github.io/palmerpenguins/

    import matplotlib.pyplot as plt
    import numpy as np

    species = ("Adelie", "Chinstrap", "Gentoo")
    penguin_means = {
        'Bill Depth': (18.35, 18.43, 14.98),
        'Bill Length': (38.79, 48.83, 47.50),
        'Flipper Length': (189.95, 195.82, 217.19),
    }

    x = np.arange(len(species))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in penguin_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Length (mm)')
    ax.set_title('Penguin attributes by species')
    ax.set_xticks(x + width, species)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 250)

    plt.show()

def chart_core(input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from CORE...[/green]')
    
    charts = []
    suffixes = []
    
    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='CORE',
                 value_fields= ["CORE_PREC","CORE_SREC","CORE_RQD"],
                 depth_fields=['CORE_TOP','CORE_BASE'],
                 errors=errors
                 )
    c0, s0 = get_chart (df, 
                     table = "CORE",
                     x_fields = ["CORE_PREC","CORE_SREC","CORE_RQD"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c0
    suffixes +=s0
    
    if 'group' in layouts: 
        c1, s1 = get_chart_grouped (df,
                        table = "CORE",
                        x_fields = ["CORE_RQD"],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        
        charts += c1
        suffixes +=s1

    return charts, suffixes

def chart_dcpt(input_file, tables, formats, layouts, errors):
    
    from .AGSData import calc_depth_dcpg

    rprint('[green] Getting chart from DCPT...[/green]')

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables = tables, 
                     table = 'DCPT',
                     value_fields = ['DCPT_CBLO'],
                     depth_fields = ['DCPG_DPTH'],
                     calc_depth = calc_depth_dcpg,
                     errors = errors)
    
    df['LOCA_ID_DCPG_TESN'] = df['LOCA_ID']+df['DCPG_TESN'].astype(str)
    
    c0, s0 = get_chart_grouped (df,
                     table = 'DCPT',
                     x_fields = ['DCPT_CBLO'],
                     group_by = ['LOCA_ID_DCPG_TESN'],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    
    return c0, s0

def chart_dcpg (input_file, tables, formats, layouts, errors):
    
    rprint('[green] Getting chart from DCPG...[/green]')
    
    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables = tables, 
                     table = 'DCPG',
                     value_fields = ['DCPG_DATE','DCPG_TESN','DCPG_ZERO'],
                     depth_fields = ["DCPG_DPTH"],
                     errors = errors)
    
    df['LOCA_ID_DCPG_TESN'] = df['LOCA_ID']+df['DCPG_TESN'].astype(str)
    
    c0, s0 = get_chart_grouped (df,
                     table = 'DCPG',
                     x_fields = ['DCPG_ZERO'],
                     group_by = ['LOCA_ID_DCPG_TESN'],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    
    return c0, s0

def chart_eres(input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from ERES...[/green]')
    
    charts = []
    suffixes = []

    #TO DO Create bar chart of eres results 
    
    return charts, suffixes
    
    if tables is None:
        tables, headers = AGS4.AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='ERES',
                 value_fields= ['ERES_RVAL'],
                 errors=errors
                 )
    
    df['LOCA_ID_ERES_CODE'] = df['LOCA_ID'] + df['ERES_CODE']

    df1 = df.loc[df['HEADING']=='DATA']

    unique_eres_code =  df1['ERES_CODE'].unique()

    for eres_code in unique_eres_code:
        df2 = df1.loc[df1['ERES_CODE']==eres_code]
        c0, s0 = get_chart (df2, 
                        table = 'ERES',
                        x_fields = ['ERES_RVAL'],
                        get_units = get_units_eres,
                        get_value_name = get_value_name_eres,
                        formats = formats, 
                        layouts = layouts,
                        errors = errors) 
        charts.append(c0)
        suffixes.append(s0)
        
        c1,s1 = get_chart_grouped (df2,
                                   table='ERES',
                                   x_fields=['ERES_RVAL'],
                                   get_units=get_units_eres,
                                   get_value_name=get_value_name_eres,
                                   formats = formats, 
                                   layouts = layouts,
                                   errors = errors)
        charts.append(c1)
        suffixes.append (s1)

    return charts, suffixes

def chart_gchm(input_file, tables, formats, layouts, errors):
   
    
    rprint('[green] Getting chart from GCHM...[/green]')
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='GCHM',
                 value_fields= ['GCHM_RESL'],
                 errors=errors
                 )
    
    df['LOCA_ID_GCHM_CODE'] = df['LOCA_ID'] + df['GCHM_CODE']
    
    df1 = df.loc[df['HEADING']=='DATA']

    unique_gchm_code =  df1['GCHM_CODE'].unique()

    for gchm_code in unique_gchm_code:

        df2 = df1.loc[df1['GCHM_CODE'] == gchm_code]

        c0, s0 = get_chart (df2, 
                        table = 'GCHM',
                        x_fields = ['GCHM_RESL'],
                        get_units = get_units_gchm,
                        get_value_name = get_value_name_gchm,
                        formats = formats, 
                        layouts = layouts,
                        errors = errors) 
        charts += c0
        suffixes += s0
        
        c1,s1 = get_chart_grouped (df2,
                                   table='GCHM',
                                   x_fields=['GCHM_RESL'],
                                   get_units=get_units_gchm,
                                   get_value_name=get_value_name_gchm,
                                   formats = formats, 
                                   layouts = layouts,
                                   errors = errors)
        charts += c1
        suffixes += s1

    return charts, suffixes

def chart_ispt(input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from ISPT...[/green]')
    
    charts = []
    suffixes = []
    
    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='ISPT', 
                 value_fields = ['ISPT_NVAL'],
                 depth_fields = ['ISPT_TOP'],
                 errors=errors
                 )
    print (df[df['ISPT_NVAL'] == ''])

    c0, s0 = get_chart (df,
                     table = 'ISPT',
                     x_fields = ['ISPT_NVAL'],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c0
    suffixes += s0
    
    if 'group' in layouts: 
        c1, s1 = get_chart_grouped (df,
                                    table = "ISPT",
                                    x_fields = ["ISPT_NVAL"],
                                    formats = formats, 
                                    layouts = layouts,
                                    errors = errors)
        charts += c1
        suffixes += s1
        
    return charts, suffixes


def chart_llpl(input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from LLPL...[/green]')
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='LLPL',
                 value_fields= ["LLPL_LL","LLPL_PL","LLPL_PI"],
                 depth_fields=['SAMP_TOP','SPEC_DPTH'],
                 errors=errors
                 )
    
    c0, s0 = get_chart (df, 
                     table = "LLPL",
                     x_fields = ["LLPL_LL","LLPL_PL"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c0
    suffixes +=s0
    
    c1, s1 = get_chart (df, 
                     table = "LLPL",
                     x_fields = ["LLPL_PI"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c1
    suffixes +=s1
    
    if 'group' in layouts: 
        c2, s2 = get_chart_grouped (df,
                        table = "LLPL",
                        x_fields = ["LLPL_PI"],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c2
        suffixes +=s2

    return charts, suffixes

def chart_lden(input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from LDEN...[/green]')
   
    charts = []
    suffixes = []
    
    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='LDEN',
                 value_fields= ["LDEN_BDEN","LDEN_DDEN","LDEN_MC"],
                 depth_fields=['SAMP_TOP','SPEC_DPTH'],
                 errors=errors
                 )
    
    c0, s0 = get_chart (df, 
                     table = "LDEN",
                     x_fields = ["LDEN_BDEN","LDEN_DDEN"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c0
    suffixes += s0
    
    c1, s1= get_chart (df, 
                     table = "LDEN",
                     x_fields = ["LDEN_MC"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c1
    suffixes += s1
    
    if 'group' in layouts:
        c2, s2 = get_chart_grouped (df,
                        table = "LLPL",
                        x_fields = ["LDEN_BDEN","LDEN_DDEN"],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c2
        suffixes += s2
        
        c3, s3 = get_chart_grouped (df,
                        table = "LLPL",
                        x_fields = ["LDEN_MC"],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c3
        suffixes += s3

    return charts, suffixes

def chart_lnmc(input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from LNMC...[/green]')
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='LNMC',
                 value_fields= ["LNMC_MC"],
                 depth_fields=['SAMP_TOP','SPEC_DPTH'],
                 errors=errors
                 )
    
    c0, s0 = get_chart (df, 
                     table = "LNMC",
                     x_fields = ["LNMC_MC"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts +=c0
    suffixes +=s0

    if 'group' in layouts:
        c1, s1 = get_chart_grouped (df,
                        table = "LNMC",
                        x_fields = ["LNMC_MC"],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c1
        suffixes +=s1

    return charts, suffixes

def chart_lvan (input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from LVAN...[/green]')
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='LVAN',
                 value_fields= ['LVAN_VNPK','LVAN_VNRM','LVAN_MC'],
                 depth_fields=['SAMP_TOP','SPEC_DPTH'],
                 errors=errors
                 )
    
    c0, s0 = get_chart (df, 
                     table = "LVAN",
                     x_fields = ['LVAN_VNPK','LVAN_VNRM'],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c0
    suffixes +=s0
    
    c1, s1 = get_chart (df, 
                     table = "LVAN",
                     x_fields = ["LVAN_MC"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c1
    suffixes +=s1
    
    if 'group' in layouts:
        c2, s2 = get_chart_grouped (df,
                        table = "LVAN",
                        x_fields = ['LVAN_VNPK','LVAN_VNRM'],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c2
        suffixes +=s2

        c3, s3 = get_chart_grouped (df,
                     table = "LVAN",
                     x_fields = ["LVAN_MC"],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
        charts += c3
        suffixes +=s3

    return charts, suffixes



def chart_mond(input_file, tables, formats, layouts, errors):
   
    import datetime as dt
    import pandas as pd

    rprint('[green] Getting chart from MOND...[/green]')
    
    dt_map = {'yyyy-mm-ddThh:mm:ss':'%Y-%m-%d %H:%M:%S',
             'yyyy-mm-ddThh:mm:ss.sssZ(+hh:mm)':'%Y-%m-%d %H:%M:%S' } 
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='MOND',
                 value_fields= ['MOND_RDNG'],
                 depth_fields=['MONG_DIS'],
                 errors=errors
                 )
    
    # df['datetime'] = df['MOND_DTIM'].str.replace('T',' ')

    df['LOCA_ID_MOND_TYPE'] = df['LOCA_ID'] + df['MOND_TYPE']
    
    df_units = df[df['HEADING']=='UNIT']
    
    dt_format = dt_map[df_units['MOND_DTIM'][0]]
    
    df1 = df.loc[df['HEADING']=='DATA']

    df1['datetime']= pd.to_datetime(df1['MOND_DTIM'], format=dt_format)
    
    print (df1['datetime'],df1['MOND_DTIM'])

    unique_mond_types =  df1['MOND_TYPE'].unique()

    for mond_type in unique_mond_types:
        df2 = df1.loc[df1['MOND_TYPE'] == mond_type]
        c0, s0 = get_chart (df2, 
                        table = 'MOND',
                        x_fields = ['datetime'],
                        y_fields = ['MOND_RDNG'],
                        get_units = get_units_mond,
                        get_value_name = get_value_name_mond,
                        formats = formats, 
                        layouts = ['a4 landscape','x_datetime:y_value'],
                        errors = errors) 
        charts += c0
        suffixes += s0

        if 'group' in layouts:
            c1, s1 = get_chart_grouped (df2, 
                            table = 'MOND',
                            x_fields = ['datetime'],
                            y_fields = ['MOND_RDNG'],
                            get_units = get_units_mond,
                            get_value_name = get_value_name_mond,
                            formats = formats, 
                            layouts = ['a4 landscape x_datetime:y_value'],
                            errors = errors) 
            charts += c1
            suffixes += s1

    return charts, suffixes

def chart_rden(input_file, tables, formats, layouts, errors):
   
    rprint('[green] Getting chart from RDEN...[/green]')
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='RDEN',
                 value_fields= ['RDEN_MC','RDEN_SMC','RDEN_BDEN','RDEN_DDEN','RDEN_PORO','RDEN_PDEN'],
                 depth_fields=['SAMP_TOP','SPEC_DPTH'],
                 errors=errors
                 )
    
    c0, s0 = get_chart (df, 
                     table = 'RDEN',
                     x_fields = ['RDEN_BDEN','RDEN_DDEN','RDEN_PDEN'],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c0
    suffixes += s0

    c1, s1= get_chart (df, 
                     table = 'RDEN',
                     x_fields = ['RDEN_MC','RDEN_SMC','RDEN_PORO'],
                     formats = formats, 
                     layouts = layouts,
                     errors = errors)
    charts += c1
    suffixes += s1
    
    if 'group' in layouts:
        c2, s2 = get_chart_grouped (df,
                        table = 'RDEN',
                        x_fields = ['RDEN_BDEN','RDEN_DDEN','RDEN_PDEN'],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c2
        suffixes += s2
        c3, s3 = get_chart_grouped (df,
                        table = "RDEN",
                        x_fields = ['RDEN_MC','RDEN_SMC','RDEN_PORO'],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c3
        suffixes += s3

    return charts, suffixes


def chart_trit(input_file, tables, formats, layouts, errors):
    
    rprint('[green] Getting chart from TRIT...[/green]')
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df = get_df (tables=tables,
                 table='TRIT',
                 depth_fields = ["SAMP_TOP","SPEC_DPTH"],
                 errors=errors
                 )
    c0, s0 =  get_chart (df=df,
                        table = 'TRIT',
                        x_fields= ['TRIT_BDEN','TRIT_DDEN'],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
    charts += c0
    suffixes +=s0
    
    if 'group' in layouts:
        c1, s1 =  get_chart_grouped (df=df,
                            table = "TRIT",
                            x_fields = ["TRIT_CU"],
                            formats = formats, 
                            layouts = layouts,
                            errors = errors)
        charts += c1
        suffixes +=s1

    return charts, suffixes

def replace_inlist(current_list, match_list, replace_list):
    new_list = current_list.copy()
    for i in range(len(new_list)):
        for j in range (len(match_list)):
            if new_list[i]==match_list[j]:
                new_list[i] = replace_list[j]

    return new_list

def chart_wstd (input_file, tables, formats, layouts, errors):
    
    import pandas as pd
    from .AGSData import calc_depth_wstd

    rprint('[green] Getting chart from WSTD...[/green]')
    
    charts = []
    suffixes = []

    if tables is None:
        tables, headers = AGS4_to_dataframe (input_file, get_line_numbers=False)
    
    df0 = get_df (tables=tables,
                 table='WSTD',
                 value_fields= ['WSTD_NMIN'],
                 depth_fields= ['WSTG_DPTH'],
                 calc_depth = calc_depth_wstd,
                 errors=errors
                 )
    
    df0['LOCA_ID_WSTG_DPTH'] = df0['LOCA_ID'] + df0['WSTG_DPTH']
    
    df1 = df0.drop_duplicates(subset=['LOCA_ID_WSTG_DPTH'], keep=False)
    
    for index, values in df1.query ("HEADING == 'DATA'").iterrows():
        curr_depth = values['depth']
        curr_level = values['level']
        new_depth = values['WSTG_DPTH'] 
        new_level = curr_level + (curr_depth-new_depth) 
        df1.at[index,'WSTD_NMIN'] = 0
        df1.at[index,'WSTD_POST'] = new_depth
        df1.at[index, 'depth'] = new_depth
        df1.at[index,'level'] = new_level

    frames = [df0, df1]
    df3 = pd.concat(frames)
    layouts
    if len(df3.index) > 0:
        c0, s0 = get_chart_grouped (df3, 
                        table = "WSTD",
                        x_fields = ['WSTD_NMIN'],
                        group_by = ['LOCA_ID_WSTG_DPTH'],
                        formats = formats, 
                        layouts = layouts,
                        errors = errors)
        charts += c0
        suffixes += s0

    return charts, suffixes
    