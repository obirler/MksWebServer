from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image, Table, Paragraph
from reportlab.pdfgen import canvas
import models
import dbexecutor
import config
import util


class FormStockMovesTemplate:
    incomingform = None
    logopath = config.AppRoot + '/static/img/mkskablo.png'
    pdfname = config.AppRoot + '/static/data/form.pdf'
    pdf = None
    styles = getSampleStyleSheet()
    entrylist = None
    columnlist = None
    doctitle = None
    tresholdcolsize = 5
    maxvsize = 490
    maxhsize = 750
    stocktypesize = 130
    stockcolorsize = 80
    stockquantitysize = 90
    stockpackagequantitysize = 90
    userfullnamesize = 85
    corporationsize = 120
    movetypesize = 110
    stockroomsize = 100
    shipinfosize = 100
    decriptionsize = 100
    datesize = 95

    def __init__(self, entrylist, columnlist, doctitle):
        """
        Instantiates a new instance of IncomingStockFormTemplate class
        :param entrylist: The list of id of stockbase entries
        :type entrylist: list[int]
        :param columnlist: The list of id of columns selected by user
        :type columnlist: list[int]
        :param doctitle: The title of the document
        :type doctitle: str
        """
        self.entrylist = entrylist
        self.columnlist = columnlist
        self.doctitle = doctitle

        if len(self.columnlist) > self.tresholdcolsize:
            # Horizontal A4 Page
            self.pdf = SimpleDocTemplate(self.pdfname, pagesize=(A4[1], A4[0]))
        else:
            # Vertical A4 Page
            self.pdf = SimpleDocTemplate(self.pdfname, pagesize=A4)

        pdfmetrics.registerFont(TTFont('MyCalibri', config.AppRoot + '/static/webfonts/CALIBRI.ttf'))
        pdfmetrics.registerFont(TTFont('MyCalibriBold', config.AppRoot + '/static/webfonts/CALIBRI-BOLD.ttf'))

    def generatePdf(self):
        elems = []
        headertable = self.createheadertable()

        bodytable = self.createbodytable()
        # signaturetable = self.createsignaturetable()

        elems.append(headertable)
        elems.append(bodytable)
        # elems.append(signaturetable)
        self.pdf.build(elems)

        return self.pdfname

    def createheadertable(self):
        headerdata = [
            [self.getlogo(), self.gettitle(), '', 'BELGE TARİHİ'],
            ['', '', '', self.getdate()]
        ]

        hwidth = 0

        if len(self.columnlist) > self.tresholdcolsize:
            # Horizontal A4 Page
            hwidth = (self.maxhsize - 120 - 130) / 2.0
        else:
            # Vertical A4 Page
            hwidth = (self.maxvsize - 120 - 130) / 2.0

        header = Table(headerdata, colWidths=[120, hwidth, hwidth, 130])
        headerstyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (0, 1)),  # Header-left image
            ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 1), 'CENTER'),
            ('SPAN', (1, 0), (2, 1)),  # Header-center title
            ('ALIGN', (1, 0), (2, 1), 'CENTER'),
            ('VALIGN', (1, 0), (2, 1), 'MIDDLE'),
            ('BOTTOMPADDING', (1, 0), (2, 1), 15),
            ('VALIGN', (3, 0), (-1, 1), 'MIDDLE'),  # Header-right date
            ('ALIGN', (3, 0), (-1, 1), 'CENTER'),
            ('FONTNAME', (3, 0), (-1, 1), 'MyCalibriBold'),
            ('FONTSIZE', (3, 0), (-1, 1), 14),
            ('SPAN', (0, 2), (3, 2)),  # Come from title
            ('BOTTOMPADDING', (0, 2), (1, 2), 7),
            ('VALIGN', (0, 2), (1, 2), 'MIDDLE')
        ]
        header.setStyle(headerstyle)
        return header

    def createbodytable(self):
        bodydata = []

        headerlist = []

        sizelist = []

        if 1 in self.columnlist:
            headerlist.append(self.getstocktableheader('MALZEMENİN CİNSİ'))
            sizelist.append(self.stocktypesize)

        if 2 in self.columnlist:
            headerlist.append(self.getstocktableheader('RENGİ'))
            sizelist.append(self.stockcolorsize)

        if 3 in self.columnlist:
            headerlist.append(self.getstocktableheader('MİKTARI'))
            sizelist.append(self.stockquantitysize)

        if 4 in self.columnlist:
            headerlist.append(self.getstocktableheader('AMBALAJ SAYISI'))
            sizelist.append(self.stockpackagequantitysize)

        if 5 in self.columnlist:
            headerlist.append(self.getstocktableheader('KULLANICI ADI'))
            sizelist.append(self.userfullnamesize)

        if 6 in self.columnlist:
            headerlist.append(self.getstocktableheader('ŞİRKET İSMİ'))
            sizelist.append(self.corporationsize)

        if 7 in self.columnlist:
            headerlist.append(self.getstocktableheader('HAREKET TİPİ'))
            sizelist.append(self.movetypesize)

        if 8 in self.columnlist:
            headerlist.append(self.getstocktableheader('AMBAR'))
            sizelist.append(self.stockroomsize)

        if 9 in self.columnlist:
            headerlist.append(self.getstocktableheader('ARAÇ BİLGİLERİ'))
            sizelist.append(self.shipinfosize)

        if 10 in self.columnlist:
            headerlist.append(self.getstocktableheader('AÇIKLAMA'))
            sizelist.append(self.decriptionsize)

        if 11 in self.columnlist:
            headerlist.append(self.getstocktableheader('TARİH'))
            sizelist.append(self.datesize)

        bodydata.append(headerlist)

        totalsize = 0

        for size in sizelist:
            totalsize += size

        if len(self.columnlist) > self.tresholdcolsize:
            # Horizontal A4 Page
            unitsize = self.maxhsize / totalsize
        else:
            # Vertical A4 Page
            unitsize = self.maxvsize / totalsize

        colwidths = []

        for size in sizelist:
            colwidths.append(size*unitsize)

        bodystyle = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 7)
        ]
        i = 0

        for ertyid in self.entrylist:
            stockbase = dbexecutor.getStockBase(ertyid)
            formstockbase = dbexecutor.getFormStockBasesByStockBaseId(stockbase.id)
            stockform = dbexecutor.getStockForm(formstockbase.stockformid)

            bodyrowlist = []
            if 1 in self.columnlist:
                bodyrowlist.append(self.getstockentry(stockbase.getStockTypeName()))

            if 2 in self.columnlist:
                bodyrowlist.append(self.getstockentry(stockbase.getStockColorName()))

            if 3 in self.columnlist:
                bodyrowlist.append(self.getstockentry(stockbase.getQuantityText()))

            if 4 in self.columnlist:
                bodyrowlist.append(self.getstockentry(formstockbase.getPackageQuantityText()))

            if 5 in self.columnlist:
                userfullname = dbexecutor.getUser(stockbase.userid).getFullName()
                bodyrowlist.append(self.getstockentry(userfullname))

            if 6 in self.columnlist:
                bodyrowlist.append(self.getstockentry(stockform.getCorporationName()))

            if 7 in self.columnlist:
                if stockbase.actiontype:
                    bodyrowlist.append(self.getstockentry('Depo Giriş Formu'))
                else:
                    bodyrowlist.append(self.getstockentry('Ürün Sevkiyat Formu'))

            if 8 in self.columnlist:
                if stockbase.actiontype:
                    bodyrowlist.append(self.getstockentry('-'))
                else:
                    outgoingstockform = dbexecutor.getOutgoingStockFormByStockFormId(stockform.id)
                    bodyrowlist.append(self.getstockentry(outgoingstockform.getStockroomName()))

            if 9 in self.columnlist:
                if stockbase.actiontype:
                    bodyrowlist.append(self.getstockentry('-'))
                else:
                    outgoingstockform = dbexecutor.getOutgoingStockFormByStockFormId(stockform.id)
                    bodyrowlist.append(self.getstockentry(outgoingstockform.shipinfo))

            if 10 in self.columnlist:
                bodyrowlist.append(self.getstockentry(formstockbase.note))

            if 11 in self.columnlist:
                bodyrowlist.append(self.getstockentry(stockbase.createdate.strftime('%d.%m.%Y %I:%M:%S')))

            i = i + 1
            bodydata.append(bodyrowlist)

        body = Table(bodydata, colWidths=colwidths, spaceBefore=0)
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
                                             parent=self.styles['Normal'], leading=24, alignment=TA_CENTER)
        titleparagraph = Paragraph(self.doctitle, titleparagrapfstyle)
        return titleparagraph

    def getdate(self):
        date = util.turkishTimeNow()
        dateparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibri', fontSize=12,
                                            parent=self.styles['Normal'], alignment=TA_CENTER)
        dateparagraph = Paragraph(date.strftime('%d.%m.%Y %I:%M:%S'), dateparagrapfstyle)
        return dateparagraph

    def getcomefrom(self):
        stockform = self.incomingform.getStockForm()
        getcomefromparagrapfstyle = ParagraphStyle(name='center', fontName='MyCalibriBold', fontSize=14,
                                                   parent=self.styles['Normal'], alignment=TA_LEFT)
        getcomefromparagraph = Paragraph(stockform.getCorporationName(), getcomefromparagrapfstyle)
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
