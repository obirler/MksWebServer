from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image, Table, Paragraph
import models
import dbexecutor
import config


class IncomingStockFormTemplate:
    incomingform = None
    logopath = config.AppRoot + '/static/img/mkskablo.png'
    pdfname = None
    pdf = None
    styles = getSampleStyleSheet()
    rownumber = 18

    def __init__(self, incomingform, rownumber):
        """
        Instantiates a new instance of IncomingStockFormTemplate class

        :param incomingform: The incoming StockForm
        :type incomingform: models.StockForm
        :param rownumber: The total number of row to be added in the document
        :type rownumber: int
        """
        self.incomingform = incomingform
        self.rownumber = rownumber
        self.pdfname = config.AppRoot + '/static/data/form.pdf'
        self.pdf = SimpleDocTemplate(self.pdfname, pagesize=A4)
        pdfmetrics.registerFont(TTFont('MyCalibri', config.AppRoot + '/static/webfonts/CALIBRI.ttf'))
        pdfmetrics.registerFont(TTFont('MyCalibriBold', config.AppRoot + '/static/webfonts/CALIBRI-BOLD.ttf'))

    def generatePdf(self):
        elems = []
        headertable = self.createheadertable()
        bodytable = self.createbodytable()
        signaturetable = self.createsignaturetable()

        elems.append(headertable)
        elems.append(bodytable)
        elems.append(signaturetable)
        self.pdf.build(elems)
        return self.pdfname

    def createheadertable(self):
        headerdata = [
            [self.getlogo(), self.gettitle(), '', 'TARİH'],
            ['', '', '', self.getdate()],
            [self.getcomefromtitle(), '', '', '']
        ]

        header = Table(headerdata, [120, 70, 230, 130], [35, 35, 30])
        headerstyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (0, 1)),  # Header-left image
            ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 1), 'CENTER'),
            ('SPAN', (1, 0), (2, 1)),  # Header-center title
            ('ALIGN', (1, 0), (2, 1), 'CENTER'),
            ('VALIGN', (1, 0), (2, 1), 'MIDDLE'),
            ('BOTTOMPADDING', (1, 0), (2, 1), 25),
            ('VALIGN', (3, 0), (-1, 1), 'MIDDLE'),  # Header-right date
            ('ALIGN', (3, 0), (-1, 1), 'CENTER'),
            ('FONTNAME', (3, 0), (-1, 1), 'MyCalibriBold'),
            ('FONTSIZE', (3, 0), (-1, 1), 14),
            ('SPAN', (0, 2), (3, 2)),  # Come from title
            ('BOTTOMPADDING', (0, 2), (1, 2), 7),
            ('VALIGN', (0, 2), (1, 2), 'MIDDLE'),
            ('VALIGN', (0, 4), (4, 4), 'MIDDLE'),  # Form table Headers
            ('ALIGN', (0, 4), (4, 4), 'CENTER')
        ]
        header.setStyle(headerstyle)
        return header

    def createbodytable(self):
        bodydata = []
        bodydata.append([self.getcountheader(), self.getstocktableheader('MALZEMENİN CİNSİ'),
                         self.getstocktableheader('RENGİ'), self.getstocktableheader('MİKTARI'),
                         self.getstocktableheader('AMBALAJ SAYISI'), self.getnoteheader()])

        rowheights = []
        rowheights.append(23)

        bodystyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 7)
        ]

        i = 0
        stockbases = dbexecutor.getStockBasesFromStockFormId(self.incomingform.id)
        for stockbase in stockbases:
            bodydata.append([self.getstockentry(str(i+1)), self.getstocktypeentry(stockbase.stocktype.name),
                             self.getstockentry(stockbase.stockcolor.name),
                             self.getstockentry(stockbase.getQuantityText()),
                             self.getstockentry(stockbase.getPackageQuantityText()),
                             self.getstockentry(stockbase.note)])
            rowheights.append(27)
            i = i + 1

        while i < self.rownumber:
            bodydata.append([self.getstockentry(str(i+1)), '', '', '', '', ''])
            rowheights.append(27)
            i = i + 1

        body = Table(bodydata, [40, 190, 60, 65, 70, 125], spaceBefore=0)
        # body = Table(bodydata, [210, 100, 120, 120], rowheights, spaceBefore=0)
        body.setStyle(bodystyle)
        return body

    def createsignaturetable(self):
        signaturedata = [
            [self.getsignatureitem('TESLİM EDEN: '),
             self.getsignatureitem('TESLİM ALAN: ')],
            [self.getsignatureitem('İMZA: '), self.getsignatureitem('İMZA: ')]
        ]

        signaturestyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]

        signature = Table(signaturedata, [275, 275], [25, 25], spaceBefore=20)
        signature.setStyle(signaturestyle)
        return signature

    def getlogo(self):
        picture = Image(self.logopath)
        picture.drawWidth = 110
        picture.drawHeight = 55
        return picture

    def gettitle(self):
        titleparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=26,
                                             parent=self.styles['Normal'], alignment=TA_CENTER)
        titleparagraph = Paragraph('DEPO GİRİŞ FORMU', titleparagrapfstyle)
        return titleparagraph

    def getdate(self):
        dateparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=12,
                                            parent=self.styles['Normal'], alignment=TA_CENTER)
        dateparagraph = Paragraph(self.incomingform.recorddate.strftime('%d.%m.%Y %I:%M:%S'), dateparagrapfstyle)
        return dateparagraph

    def getcomefromtitle(self):
        getcomefromtitleparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                        parent=self.styles['Normal'], alignment=TA_LEFT)
        getcomefromtitleparagraph = Paragraph('MALZEMENİN GELDİĞİ YER: ' + self.incomingform.corporation.name,
                                              getcomefromtitleparagrapfstyle)
        return getcomefromtitleparagraph

    def getcomefrom(self):
        getcomefromparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                   parent=self.styles['Normal'], alignment=TA_LEFT)
        getcomefromparagraph = Paragraph(self.incomingform.corporation.name, getcomefromparagrapfstyle)
        return getcomefromparagraph

    def getcountheader(self):
        countparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                  parent=self.styles['Normal'], alignment=TA_CENTER)
        counttableparagraph = Paragraph('SIRA NO', countparagrapfstyle)
        return counttableparagraph

    def getnoteheader(self):
        paragrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                        parent=self.styles['Normal'], alignment=TA_CENTER)
        paragraph = Paragraph('AÇIKLAMA', paragrapfstyle)
        return paragraph

    def getstocktableheader(self, headername):
        stocktableparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                  parent=self.styles['Normal'], alignment=TA_CENTER)
        stocktableparagraph = Paragraph(headername, stocktableparagrapfstyle)
        return stocktableparagraph

    def getstocktypeentry(self, description):
        typeparagraphstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=12,
                                            parent=self.styles['Normal'], alignment=TA_LEFT)
        typeparagraph = Paragraph(description, typeparagraphstyle)
        return typeparagraph

    def getstockentry(self, stockproperty):
        stockparagraphstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=12,
                                             parent=self.styles['Normal'], alignment=TA_CENTER)
        stockparagraph = Paragraph(stockproperty, stockparagraphstyle)
        return stockparagraph

    def getsignatureitem(self, prop):
        signatureparagraphstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=10,
                                                 parent=self.styles['Normal'], alignment=TA_LEFT)
        signatureparagraph = Paragraph(prop, signatureparagraphstyle)
        return signatureparagraph
