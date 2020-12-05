from reportlab.platypus import SimpleDocTemplate, Image, Table, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
import models
import dbexecutor
import config


class OutgoingStockFormTemplate:
    outgoingform = None
    logopath = config.AppRoot + '/static/img/mkskablo.png'
    pdfname = None
    pdf = None
    styles = getSampleStyleSheet()
    rownumber = 18

    def __init__(self, outgoingform, rownumber):
        """
        Instantiates a new instance of OutgoingStockFormTemplate class
        :param outgoingform: OutgoingStockForm
        :type outgoingform: models.OutgoingStockForm
        """
        self.outgoingform = outgoingform
        self.rownumber = rownumber
        self.pdfname = config.AppRoot + '/static/data/form.pdf'
        self.pdf = SimpleDocTemplate(self.pdfname, pagesize=A4)
        pdfmetrics.registerFont(TTFont('MyCalibri', config.AppRoot + '/static/webfonts/CALIBRI.ttf'))
        pdfmetrics.registerFont(TTFont('MyCalibriBold', config.AppRoot + '/static/webfonts/CALIBRI-BOLD.ttf'))

    def generatePdf(self):
        elems = []
        headertable = self.createheadertable()
        bodytable = self.createbodytable()
        note = self.getnoteparagraph()
        signaturetable = self.createsignaturetable()

        elems.append(headertable)
        elems.append(bodytable)
        elems.append(note)
        elems.append(signaturetable)
        self.pdf.build(elems)
        return self.pdfname

    def createheadertable(self):
        headerdata = [
            [self.getlogo(), '', self.gettitle(), '', '', '', 'TARİH'],
            ['', '', '', '', '', '', self.getdate()],
            [self.getgoingtoinfo(), '', '', '', '', '', self.getstockroomshipinfo()],
            [self.getcountheader(), self.getstocktableheader('MALZEMENİN CİNSİ'), '', self.getstocktableheader('RENGİ'),
             self.getstocktableheader('MİKTARI'), self.getstocktableheader('AMBALAJ SAYISI'), ''],
            ['', '', '', '', '', '', self.getstocktableheader('AÇIKLAMA')]
        ]

        header = Table(headerdata, [40, 80, 110, 60, 65, 70, 125])
        headerstyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (1, 1)),  # Header-left image
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (1, 1), 'CENTER'),
            ('SPAN', (2, 0), (5, 1)),  # Header-center title
            ('ALIGN', (2, 0), (5, 1), 'CENTER'),
            ('BOTTOMPADDING', (2, 0), (5, 1), 25),
            ('ALIGN', (6, 0), (6, 0), 'CENTER'),  # Header-right date
            ('FONTNAME', (6, 0), (6, 0), 'MyCalibriBold'),
            ('FONTSIZE', (6, 0), (6, 0), 14),
            ('SPAN', (0, 2), (5, 2)),  # Come from title
            ('BOTTOMPADDING', (0, 2), (5, 2), 7),
            ('SPAN', (6, 2), (6, 3)),  # stockroom section
            ('SPAN', (0, 3), (0, 4)),  # count section
            ('SPAN', (1, 3), (2, 4)),  # stocktype section
            ('SPAN', (3, 3), (3, 4)),  # stockcolor section
            ('SPAN', (4, 3), (4, 4)),  # stockquantity section
            ('SPAN', (5, 3), (5, 4)),  # stockpackage section
            ('BOTTOMPADDING', (6, 4), (6, 4), 9)
        ]
        header.setStyle(headerstyle)
        return header

    def createbodytable(self):
        bodydata = []

        rowheights = []
        rowheights.append(23)

        bodystyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7)
        ]

        i = 0
        stockform = self.outgoingform.getStockForm()
        formstockbases = dbexecutor.getFormStockBasesByStockFormId(stockform.id)
        for formstockbase in formstockbases:
            bodydata.append([self.getstockentry(str(i+1)),
                             self.getstockdecriptionentry(formstockbase.getStockTypeName()),
                             self.getstockentry(formstockbase.getStockColorName()),
                             self.getstockentry(formstockbase.getQuantityText()),
                             self.getstockentry(formstockbase.getPackageQuantityText()),
                             self.getstockentry(formstockbase.note)])
            rowheights.append(27)
            i = i + 1

        while i < self.rownumber:
            bodydata.append([self.getstockentry(str(i+1)), '', '', '', ''])
            rowheights.append(27)
            i = i + 1
        body = Table(bodydata, [40, 190, 60, 65, 70, 125], spaceBefore=0)
        body.setStyle(bodystyle)
        return body

    def createsignaturetable(self):
        signaturedata = [
            [self.getsignatureitem('HAZIRLAYANLAR:'),
             self.getsignatureitem('KONTROL EDEN:'),
             self.getsignatureitem('TESLİM EDEN:'),
             self.getsignatureitem('TESLİM ALAN:')],
            [self.getsignatureitem('İMZA:'), self.getsignatureitem('İMZA:'),
             self.getsignatureitem('İMZA:'), self.getsignatureitem('İMZA:')]
        ]

        signaturestyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 0)
        ]

        signature = Table(signaturedata, [137.5, 137.5, 137.5, 137.5], [60, 25], spaceBefore=0)
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
        titleparagraph = Paragraph('ÜRÜN SEVKİYAT FORMU', titleparagrapfstyle)
        return titleparagraph

    def getdate(self):
        stockform = self.outgoingform.getStockForm()
        dateparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=12,
                                            parent=self.styles['Normal'], alignment=TA_CENTER)
        dateparagraph = Paragraph(stockform.recorddate.strftime('%d.%m.%Y %I:%M:%S'), dateparagrapfstyle)
        return dateparagraph

    def getgoingtoinfo(self):
        getgoingtoparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                  parent=self.styles['Normal'], alignment=TA_LEFT)
        getgoingtoparagraph = Paragraph('MALZEMENİN GÖNDERİLDİĞİ YER: ' + self.outgoingform.getCorporationName(),
                                        getgoingtoparagrapfstyle)
        return getgoingtoparagraph

    def getcountheader(self):
        countparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                  parent=self.styles['Normal'], alignment=TA_CENTER)
        counttableparagraph = Paragraph('SIRA <br/>NO', countparagrapfstyle)
        return counttableparagraph

    def getstockroomshipinfo(self):
        stockroomparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14, leading=16,
                                                 parent=self.styles['Normal'], alignment=TA_LEFT)
        stockroomparagraph = Paragraph('AMBAR: ' + self.outgoingform.getStockroomName() + '<br/>ARAÇ BİLGİLERİ: ' +
                                       self.outgoingform.shipinfo, stockroomparagrapfstyle)
        return stockroomparagraph

    def getstocktableheader(self, headername):
        stocktableparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                  parent=self.styles['Normal'], alignment=TA_CENTER)
        stocktableparagraph = Paragraph(headername, stocktableparagrapfstyle)
        return stocktableparagraph

    def getstockdecriptionentry(self, description):
        descparagraphstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=12,
                                            parent=self.styles['Normal'], alignment=TA_LEFT)
        descparagraph = Paragraph(description, descparagraphstyle)
        return descparagraph

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

    def getnoteparagraph(self):
        paragrapfstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=10,
                                        parent=self.styles['Normal'], alignment=TA_LEFT)
        text = '<u>NOT:</u> BU BELGEYİ İMZALIYARAK YUKARIDA ADI GEÇEN ÜRÜNLERİ <u>EKSİKSİZ VE SAĞLAM</u> OLARAK ' \
               'ALDIĞIMI KABUL EDİYORUM. HER HANGİ BİR OLUMSUZLUKTA MADDİ VE MANEVİ TÜM ZARAR FİRMAM VE ŞAHSIM ' \
               'TARAFINDAN KARŞILANAÇAKTIR.'
        paragraph = Paragraph(text, paragrapfstyle)
        return paragraph