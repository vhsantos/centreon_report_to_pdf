from CentreonData import *
from datetime import date
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import green, lightgreen,  red,  black,  orange,  grey,  blueviolet,  silver, salmon, whitesmoke
from reportlab.lib.enums import TA_LEFT,  TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle,  getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import *
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageTemplate, FrameBreak, NextPageTemplate
from Settings import *
import sys

# Variables definitions
DOCMARGIN = 10*mm
PAGE_HEIGHT = 297*mm
PAGE_WIDTH = 210*mm
height = 297*mm
width = 210*mm

# Table row color
skyblue = "#bfecff"

# Columns variables definition
# [(start_column, start_row), (end_column, end_row)]
all_cells = [(0, 0), (-1, -1)]
header = [(0, 0), (-1, 0)]

# Columns table resume
column_state = [(0, 0), (0, -1)]
column_total_time = [(1, 0), (1, -1)]
column_mean_time = [(2, 0), (2, -1)]
column_alerts = [(3, 0), (3, -1)]

# Columns table details_SG
column_hostname = [(0, 0), (0, -1)]
column_service = [(1, 0), (1, -1)]
column_ok_percent = [(2, 0), (2, -1)]
column_ok_alerts = [(3, 0), (3, -1)]
column_warn_percent = [(4, 0), (4, -1)]
column_warn_alerts = [(5, 0), (5, -1)]
column_critical_percent = [(6, 0), (6, -1)]
column_critical_alerts = [(7, 0), (7, -1)]
column_unknow_percent = [(8, 0), (8, -1)]
column_unknow_alerts = [(9, 0), (9, -1)]
column_scheduled_percent_sg = [(10, 0), (10, -1)]
column_undetermined_alerts_sg = [(11, 0), (11, -1)]

# Columns table details_HG
column_hostname = [(0, 0), (0, -1)]
column_up_percent = [(1, 0), (1, -1)]
column_up_alerts = [(2, 0), (2, -1)]
column_down_percent = [(3, 0), (3, -1)]
column_down_alerts = [(4, 0), (4, -1)]
column_unrechable_percent = [(5, 0), (5, -1)]
column_unrechable_alerts = [(6, 0), (6, -1)]
column_scheduled_percent_hg = [(7, 0), (7, -1)]
column_undetermined_alerts_hg = [(8, 0), (8, -1)]

# create a empty variable
doc = None


########################################
########################################
# TODO - Try diff fonts
# Function to define some styles
def stylesheet():
    """Function to define some styles"""
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Courier',
            bulletFontSize=10,
            bulletIndent=0,
            textColor=black,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
        ),
    }

    styles['cover_title'] = ParagraphStyle(
        'cover_title',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=22,
        alignment=TA_CENTER,
    )

    styles['cover_text'] = ParagraphStyle(
        'cover_text',
        fontName='Courier-Bold',
        fontSize=14,
        leading=28,
        alignment=TA_CENTER,
    )

    styles['table_default'] = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('FONTSIZE', all_cells[0], all_cells[1], 8),
        ('VALIGN', all_cells[0], all_cells[1], 'MIDDLE'),
        ('ALIGN', all_cells[0], all_cells[1], 'CENTER'),
    ]
    )

    styles['table_details_head_SG'] = TableStyle([
        ('SPAN',  (0, 0),  (0, 1)),
        ('SPAN',  (1, 0),  (1, 1)),
        ('SPAN',  (2, 0),  (3, 0)),
        ('SPAN',  (4, 0),  (5, 0)),
        ('SPAN',  (6, 0),  (7, 0)),
        ('SPAN',  (8, 0),  (9, 0)),
    ]
    )

    styles['table_details_head_HG'] = TableStyle([
        ('SPAN',  (0, 0),  (0, 1)),
        ('SPAN',  (1, 0),  (2, 0)),
        ('SPAN',  (3, 0),  (4, 0)),
        ('SPAN',  (5, 0),  (6, 0)),
    ]
    )

    styles['table_details_SG'] = TableStyle([
        # Columns names
        # column_hostname =  [(0, 0), (0, -1)]
        # column_service = [(1, 0), (1, -1)]
        # column_ok_percent = [(2, 0), (2, -1)]
        # column_ok_alerts = [(3, 0), (3, -1)]
        # column_warn_percent = [(4, 0), (4, -1)]
        # column_warn_alerts = [(5, 0), (5, -1)]
        # column_critical_percent = [(6, 0), (6, -1)]
        # column_critical_alerts = [(7, 0), (7, -1)]
        # column_unknow_percent = [(8, 0), (8, -1)]
        # column_unknow_alerts = [(9, 0), (9, -1)]
        # column_scheduled_percent = [(10, 0), (10, -1)]
        # column_undetermined_alerts = [(11, 0), (11, -1)]
        ('GRID', (0, 0), (-1, -1), 0.5, whitesmoke),
        ('ALIGN', column_hostname[0], column_hostname[1], 'LEFT'),
        ('ALIGN', column_service[0], column_service[1], 'LEFT'),
        ('ALIGN', (0, 0),  (0, 1), 'CENTER'),
        ('ALIGN', (1, 0),  (1, 1), 'CENTER'),
        ('BACKGROUND',  (2, 0),  (3, -1),  lightgreen),
        ('BACKGROUND',  (4, 0),  (5, -1),  orange),
        ('BACKGROUND',  (6, 0),  (7, -1),  red),
        ('BACKGROUND',  (8, 0),  (9, -1),  silver),
        ('BACKGROUND',  column_scheduled_percent_sg[0],
         column_scheduled_percent_sg[1],  blueviolet),
        ('BACKGROUND',
         column_undetermined_alerts_sg[0],  column_undetermined_alerts_sg[1],  salmon),
    ]
    )

    styles['table_details_HG'] = TableStyle([
        # Columns table details_HG
        # column_hostname =  [(0, 0), (0, -1)]
        # column_up_percent = [(1, 0), (1, -1)]
        # column_up_alerts = [(2, 0), (2, -1)]
        # column_down_percent = [(3, 0), (3, -1)]
        # column_down_alerts = [(4, 0), (4, -1)]
        # column_unrechable_percent = [(5, 0), (5, -1)]
        # column_unrechable_alerts = [(6, 0), (6, -1)]
        # column_scheduled_percent_hg = [(7, 0), (7, -1)]
        # column_undetermined_alerts_hg = [(8, 0), (8, -1)]
        ('GRID', (0, 0), (-1, -1), 0.5, whitesmoke),
        ('ALIGN', column_hostname[0], column_hostname[1], 'LEFT'),
        ('ALIGN', (0, 0),  (0, 1), 'CENTER'),
        ('ALIGN', (1, 0),  (1, 1), 'CENTER'),
        ('BACKGROUND',  (1, 0),  (2, -1),  lightgreen),
        ('BACKGROUND',  (3, 0),  (4, -1),  red),
        ('BACKGROUND',  (5, 0),  (6, -1),  silver),
        ('BACKGROUND',  column_scheduled_percent_hg[0],
         column_scheduled_percent_hg[1],  blueviolet),
        ('BACKGROUND',
         column_undetermined_alerts_hg[0],  column_undetermined_alerts_hg[1],  salmon),
    ]
    )

    styles['table_resume_SG'] = TableStyle([
        # Columns names
        # column_state=  [(0, 0), (0, -1)]
        # column_total_time = [(1, 0), (1, -1)]
        # column_mean_time = [(2, 0), (2, -1)]
        # column_alerts = [(3, 0), (3, -1)]
        ('FONTSIZE', all_cells[0], all_cells[1], 10),
        ('GRID', (0, 0), (-1, -1), 0.5, whitesmoke),
        ('ALIGN', column_state[0], column_state[1], 'LEFT'),
        ('BACKGROUND',  (0, 0), (-1, 1),  "#eaeaee"),
        ('TEXTCOLOR',  (0, 1),  (0, 1),  green),
        ('TEXTCOLOR',  (0, 2),  (0, 2),  orange),
        ('TEXTCOLOR',  (0, 3),  (0, 3),  red),
        ('TEXTCOLOR',  (0, 4),  (0, 4),  black),
        ('TEXTCOLOR',  (0, 5),  (0, 5),  blueviolet),
        ('TEXTCOLOR',  (0, 6),  (0, 6),  salmon),
        ('FONTNAME',  (0, 1),  (0, 1),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 2),  (0, 2),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 3),  (0, 3),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 4),  (0, 4),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 5),  (0, 5),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 6),  (0, 6),  'Helvetica-Bold'),
        ('BACKGROUND',  (0,  -1), (-1, -1),  "#eaeaee"),
    ]
    )

    styles['table_resume_HG'] = TableStyle([
        # Columns names
        # column_state =  [(0, 0), (0, -1)]
        # column_total_time = [(1, 0), (1, -1)]
        # column_mean_time = [(2, 0), (2, -1)]
        # column_alerts = [(3, 0), (3, -1)]
        ('FONTSIZE', all_cells[0], all_cells[1], 10),
        ('GRID', (0, 0), (-1, -1), 0.5, whitesmoke),
        ('ALIGN', column_state[0], column_state[1], 'LEFT'),
        ('BACKGROUND',  (0, 0), (-1, 1),  "#eaeaee"),
        ('TEXTCOLOR',  (0, 1),  (0, 1),  green),
        ('TEXTCOLOR',  (0, 2),  (0, 2),  red),
        ('TEXTCOLOR',  (0, 3),  (0, 3),  black),
        ('TEXTCOLOR',  (0, 4),  (0, 4),  blueviolet),
        ('TEXTCOLOR',  (0, 5),  (0, 5),  salmon),
        ('FONTNAME',  (0, 1),  (0, 1),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 2),  (0, 2),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 3),  (0, 3),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 4),  (0, 4),  'Helvetica-Bold'),
        ('FONTNAME',  (0, 5),  (0, 5),  'Helvetica-Bold'),
        ('BACKGROUND',  (0,  -1), (-1, -1),  "#eaeaee"),
    ]
    )

    return styles


styles = stylesheet()
styleNormal = styles['default']
styleCoverTitle = styles['cover_title']
styleCoverText = styles['cover_text']
styleTable = styles['table_default']
styleTableDetailsHead_SG = styles['table_details_head_SG']
styleTableDetails_SG = styles['table_details_SG']
styleTableDetailsHead_HG = styles['table_details_head_HG']
styleTableDetails_HG = styles['table_details_HG']
styleTableResume_SG = styles['table_resume_SG']
styleTableResume_HG = styles['table_resume_HG']


########################################
########################################
# Function to put the page number at the end of page to template 1
def foot1(canvas, doc):
    """Function to put the page number at the end of page"""
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(width-20*mm, 2*mm, "Page %d" % doc.page)
    canvas.restoreState()


# Function to put the page number at the end of page to template 2
def foot2(canvas, doc):
    """Function to put the page number at the end of page"""
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(width-20*mm, 2*mm, "Page %d" % doc.page)


########################################
########################################
# Function to generate the Pie Graph
def pie_chart_with_legend():
    """Function to generate the Pie Graph"""

    # Get the details data from CSV file
    data_df = get_centreon_csv_resume()

    # Get the values from Total Time and Status
    data_list = data_df['Total Time'].astype(float).values.tolist()
    data_labels = data_df['Status'].values.tolist()

    # Position of the Pie
    drawing = Drawing(width=10*mm, height=70*mm)

    # Set some Pie parameters
    pie = Pie()
    pie.x = 14*mm
    pie.y = 5*mm
    pie.height = 60*mm
    pie.width = 60*mm
    pie.data = data_list
    pie.labels = data_labels

    pie.sideLabels = True
    pie.slices.strokeWidth = 0.5
    pie.slices.popout = 7
    pie.startAngle = 90
    pie.sameRadii = 1
    pie.direction = 'clockwise'

    # define colors of Pie
    # If SG Report
    if GlobalVars.report_type == 'ServiceGroup':
        piecolors = [green,  orange,  red,  silver,  blueviolet,  salmon]
    # If HG Report
    elif GlobalVars.report_type == 'Hostgroup':
        piecolors = [green,  red,  silver,  blueviolet,  salmon]
    # Apply colors
    for i, color in enumerate(piecolors):
        pie.slices[i].fillColor = color

    # Create the pie
    drawing.add(pie)

    return drawing


########################################
########################################
# Function to get INFO from CSV, format and create a table
def build_table_info():
    """Function to get INFO from CSV, format and create a table"""
    # Get the data info from CSV file
    data_df = get_centreon_csv_info()

    # Create a title content
    contents_title = []

    # Get some defaults styles
    styleSheet = getSampleStyleSheet()

    # Define style to Title
    title = styleSheet['Title']
    title.fontSize = 12
    title.alignment = TA_CENTER
    title.leading = 10

    # Add the title
    contents_title.append(Paragraph(GlobalVars.report_type_name +
                          ": " + str(data_df[GlobalVars.report_type][0]), title))

    # Define style to Text
    text = styleSheet['Normal']
    text.fontSize = 10
    text.alignment = TA_CENTER
    text.leading = 14

    # Get the days between start and and
    dates_diff = data_df[' End date'] - data_df['Begin date']
    days_total = int(dates_diff.dt.days)

    # Format dates
    date_begin = data_df['Begin date'].dt.strftime('%d/%b/%Y - %H:%M:%S')
    date_end = data_df[' End date'].dt.strftime('%d/%b/%Y - %H:%M:%S')

    # Add the info to contents
    contents_title.append(
        Paragraph("Start Date: " + str(date_begin[0]),  text))
    contents_title.append(Paragraph(" End Date: " + str(date_end[0]),  text))
    contents_title.append(Paragraph("( " + str(days_total) + " Days )",  text))

    return contents_title


########################################
########################################
# Function to get RESUME data from CSV, format and create a table
def build_table_resume():
    """Function to get RESUME data from CSV, format and create a table"""
    # Get the details data from CSV file
    data_df = get_centreon_csv_resume()

    # Get the total of Alerts
    total_alerts = 0
    total_alerts = int(data_df["Alerts"].sum(skipna=True))

    # Create a extra line with "Total" at the end
    extra_table_foot = [['Total', '', '', total_alerts]]
    # Conact the header + data to list + t
    data_list = [data_df.columns.values.tolist()] + \
        data_df.values.tolist() + list(extra_table_foot)

    # Generate the table using the list and repeat the headers if necesary
    table = Table(data=data_list,  repeatRows=0, rowHeights=15)

    # Apply some styles to table and cells
    table.setStyle(styleTable)
    # If SG Report
    if GlobalVars.report_type == 'ServiceGroup':
        table.setStyle(styleTableResume_SG)
    # If HG Report
    elif GlobalVars.report_type == 'Hostgroup':
        table.setStyle(styleTableResume_HG)
    else:
        print("Can't determinte the type of report to create a table resume.")
        # Finish  :-(
        sys.exit()()

    # Get the number of rows (+1 for two lines headers)
    data_len = len(data_df) + 1

    # exchage rows background color
    for each in range(data_len):
        if each == 0:
            continue
        if each % 2 == 0:
            bg_color = whitesmoke
        else:
            bg_color = skyblue

        table.setStyle(TableStyle(
            [('BACKGROUND', (0, each), (-1, each), bg_color)]))

    return table


########################################
########################################
# Function to get DETAILS data from CSV, format and create a table
def build_table_details():
    """Function to get DETAILS data from CSV, format and create a table"""

    # Get the report type
    # If SG Report
    if GlobalVars.report_type == 'ServiceGroup':
        GlobalVars.report_type_name = 'Service Group'

        # Get the details data from CSV file
        data_df = get_centreon_csv_details_SG()

        # Create a second subhead to table
        subhead = [['', '', '%', 'Alert', '%', 'Alert',
                    '%', 'Alert', '%', 'Alert', 'Downtimes', '%']]

        for index, row in data_df.iterrows():
            data_df.loc[index, 'Host'] = Paragraph(
                str(row['Host']), styleNormal)
            data_df.loc[index, 'Service'] = Paragraph(
                str(row['Service']), styleNormal)

        # Conact the header + sub_header and data to list
        data_list = [data_df.columns.values.tolist()] + list(subhead) + \
            data_df.values.tolist()

        # Get the value of the column size for the host and service
        if GlobalVars.column_size_host == 'auto' or GlobalVars.column_size_service == 'auto':
            columns_table_sizes = ['*', '*',  10*mm,  10*mm,  10*mm,
                                   10*mm,  10*mm,  10*mm, 10*mm,  10*mm,  20*mm,  20*mm]
        # if not setup, put it on automatically (default)
        else:
            columns_table_sizes = [GlobalVars.column_size_host*mm, GlobalVars.column_size_service *
                                   mm,  10*mm,  10*mm,  10*mm,  10*mm,  10*mm,  10*mm, 10*mm,  10*mm,  20*mm,  20*mm]

        # Generate the table using the list and repeat the headers if necesary
        # Fixed hosts/services columns values are need to allow paragraph text wrap works correctly if there is no spaces.
        table = Table(data=data_list,  repeatRows=2,
                      colWidths=columns_table_sizes)

        # Apply some styles to table and cells
        table.setStyle(styleTable)
        table.setStyle(styleTableDetailsHead_SG)
        table.setStyle(styleTableDetails_SG)

    # If HG Report
    elif GlobalVars.report_type == 'Hostgroup':
        GlobalVars.report_type_name = 'Host Group'

        # Get the details data from CSV file
        data_df = get_centreon_csv_details_HG()

        # Create a second subhead to table
        subhead = [['', '%', 'Alert', '%', 'Alert',
                    '%', 'Alert', 'Downtimes', '%']]

        # Conact the header + sub_header and data to list
        data_list = [data_df.columns.values.tolist()] + list(subhead) + \
            data_df.values.tolist()

        # Generate the table using the list and repeat the headers if necesary
        table = Table(data=data_list,  repeatRows=2,  colWidths=[
                      '*',  12*mm,  12*mm,  12*mm,  12*mm,  12*mm,  12*mm,  20*mm,  20*mm])

        # Apply some styles to table and cells
        table.setStyle(styleTable)
        table.setStyle(styleTableDetailsHead_HG)
        table.setStyle(styleTableDetails_HG)

    # If None Report
    else:
        print("Can't determinte the type of report to create a table details.")
        # Finish  :-(
        sys.exit()()

    # Get the number of rows (+2 for two lines headers)
    data_len = len(data_df) + 2
    # exchage rows background color
    for each in range(data_len):
        if each == 0 or each == 1:
            continue
        if each % 2 == 0:
            bg_color = whitesmoke
        else:
            bg_color = skyblue

        # If SG change two firsts columns
        if GlobalVars.report_type == 'ServiceGroup':
            table.setStyle(TableStyle(
                [('BACKGROUND', (0, each), (1, each), bg_color)]))
        # If HG change only first columns
        elif GlobalVars.report_type == 'Hostgroup':
            table.setStyle(TableStyle(
                [('BACKGROUND', (0, each), (0, each), bg_color)]))

    return table


########################################
########################################
#  Function to build the PDF report with graph and tables
def prepare_report():
    """Function to build the PDF report with graph and tables"""

    # Define the variable contents
    contents = []

    # Initiate some variables based on the type of report (SG or HG)
    get_centreon_report_type()

    # Define frames to cover Page
    Frame_cover_image = Frame(50*mm, (height-100*mm),
                              110*mm, 55*mm, showBoundary=0)
    Frame_cover_title1 = Frame(
        30*mm, (height-150*mm), 150*mm, 20*mm, showBoundary=0)
    Frame_cover_title2 = Frame(
        30*mm, (height-170*mm), 150*mm, 20*mm, showBoundary=0)
    Frame_cover_text1 = Frame(30*mm, (height-220*mm),
                              150*mm, 40*mm, showBoundary=0)
    Frame_cover_info = Frame(30*mm, (height-270*mm),
                             150*mm, 40*mm, showBoundary=0)

    # Create a list with all frames to be in the cover page
    framesCoverPage = []
    framesCoverPage.append(Frame_cover_image)
    framesCoverPage.append(Frame_cover_title1)
    framesCoverPage.append(Frame_cover_title2)
    framesCoverPage.append(Frame_cover_text1)
    framesCoverPage.append(Frame_cover_info)

    # Define some Frames to Page 02
    Frame_Graphic = Frame(5*mm, height-80*mm,
                          (width-10*mm)/2, 75*mm, showBoundary=1)
    Frame_Info = Frame((width)/2, height-30*mm,
                       (width-10*mm)/2, 25*mm, showBoundary=1)
    Frame_Resume = Frame((width)/2, height-80*mm,
                         (width-10*mm)/2, 50*mm, showBoundary=1)
    Frame_Details = Frame(5*mm, 5*mm, (width-10*mm),
                          height-85*mm, showBoundary=1)

    # Create a list with all frames to be in the second page
    framesSecondPage = []
    framesSecondPage.append(Frame_Graphic)
    framesSecondPage.append(Frame_Info)
    framesSecondPage.append(Frame_Resume)
    framesSecondPage.append(Frame_Details)

    # Define other Frames (all page) if table_details need more than one page
    Frame_Details_Continue = Frame(
        5*mm, 5*mm, (width-10*mm), (height-10*mm), showBoundary=1)

    # Create a list with frame to be in the anothers pages
    framesOthersPages = []
    framesOthersPages.append(Frame_Details_Continue)

    # Create a list of templates and associate the frames list to it.
    templates = []

    # check if we need to add a Cover Page to templates
    if GlobalVars.include_cover_page is True:
        templates.append(PageTemplate(frames=framesCoverPage, id="coverpage"))
    templates.append(PageTemplate(frames=framesSecondPage,
                     id="secondpage", onPage=foot1))
    templates.append(PageTemplate(frames=framesOthersPages,
                     id="otherspages", onPage=foot2))

    # Add this templates to document.
    doc.addPageTemplates(templates)

    # check if we need to add a Cover Page
    if GlobalVars.include_cover_page is True:
        contents.append(NextPageTemplate('coverpage'))

        # Prepare the Cover Page
        for cover_content in prepare_cover_page():
            contents.append(cover_content)

        # Only one cover page are allowed.
        GlobalVars.include_cover_page = False

    # Next content will be on Frame_Info at second page
    contents.append(NextPageTemplate('secondpage'))

    # Create the pie graph with the resume information
    chart = pie_chart_with_legend()

    # Add the pie to contents on Frame_Graphic
    contents.append(chart)

    # Next content will be the Information on Frame_Info
    contents.append(FrameBreak())

    # Create and add INFO section
    for info_content in build_table_info():
        contents.append(info_content)

    # Next content will be the Resume on Frame_Resume
    contents.append(FrameBreak())

    # Create and add table_details on second page
    contents.append(build_table_resume())

    contents.append

    # Next content will be on Frame_Details
    contents.append(FrameBreak())

    contents.append(NextPageTemplate('otherspages'))

    # Add table_details on second page
    contents.append(build_table_details())

    contents.append(NextPageTemplate('secondpage'))
    contents.append(PageBreak())

    return contents


########################################
########################################
# Function to build the PDF cover page
def prepare_cover_page():
    """Function to build the PDF cover page"""

    # Define the variable contents
    contents = []

    # Setup the logo image
    if GlobalVars.cover_logo_file != '':
        logo = Image(GlobalVars.cover_logo_file,  GlobalVars.cover_logo_size_x *
                     mm,  GlobalVars.cover_logo_size_y * mm)
        logo._restrictSize(GlobalVars.cover_logo_size_x * mm,
                           GlobalVars.cover_logo_size_y * mm)
        logo.hAlign = 'CENTER'
        contents.append(logo)
    contents.append(FrameBreak())

    # Title first line
    contents.append(Paragraph(GlobalVars.cover_title_1, styleCoverTitle))
    contents.append(FrameBreak())

    # Title second line
    contents.append(Paragraph(GlobalVars.cover_title_2, styleCoverTitle))
    contents.append(FrameBreak())

    # Text lines
    contents.append(Paragraph(GlobalVars.cover_text_1, styleCoverText))
    contents.append(Paragraph(GlobalVars.cover_text_2, styleCoverText))
    contents.append(FrameBreak())

    # check if we need to add tech data
    if GlobalVars.cover_extra_info is True:
        # get the date from today
        today = date.today()
        contents.append(Paragraph(today.strftime(
            GlobalVars.cover_date_format), styleCoverText))
        # get the URL from configuration file.
        contents.append(Paragraph(GlobalVars.server_url, styleCoverText))

    return contents


########################################
########################################
def build_report():

    global doc

    # Output document
    doc = BaseDocTemplate(
        GlobalVars.pdf_output_file,
        pagesize=A4,
        topMargin=DOCMARGIN,
        bottomMargin=DOCMARGIN,
        leftMargin=DOCMARGIN,
        rightMargin=DOCMARGIN,
        showBoundary=0,
    )

    # Create a variable to content all story.
    all_contents = []

    # Create the URL list based on Host Groups(HG) and Service Groups (SG)
    csv_url = prepare_csv_url()

    # Download the CSV from centreon server
    for url in csv_url:
        # Download CSV
        download_csv(url)

        # Process the CSV and put the content of this doc in the story
        all_contents.extend(prepare_report())

    # Build the Document. Finally !!! :D
    doc.build(all_contents)
