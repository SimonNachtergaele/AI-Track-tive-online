from flask import request
from flask import Flask, render_template, redirect, url_for, send_from_directory, render_template 
app = Flask(__name__)

# source: https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/?ref=rp
app.config["SESSION_PERMANENT"] = False   #So this session has a default time limit of some number of minutes or hours or days after which it will expire.
app.config["SESSION_TYPE"] = "filesystem"  # It will store in the hard drive (these files are stored under a /flask_session folder in your config directory.) or any online ide account and it is an alternative to using a Database or something else like that.
app.config["SESSION_FILE_DIR"] = "/home/aiuser/aitracktive/flask_session"

# Import some stuff for our sessions 
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

Session(app)

import cv2

# Import logging
import logging
import datetime
from datetime import datetime
 
now = datetime.now()
today = now.strftime("%Y%m%d")
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='/home/aiuser/aitracktive/logs/'+today+'_aitracktive.log',
                filemode='a')


#--------------------------------------------------------------------------------------------
# ---------------------------------- FORM FOR TRACK COUNTING--------------------------------- 
# -------------------------------------------------------------------------------------------

from wtforms import (Form, StringField, validators, SubmitField, SelectField)
from wtforms.validators import DataRequired

class SettingsForm(Form):
    """User entry form for entering specifics for generation"""
    # Name 
    name = StringField("Enter your sample name", validators=[validators.InputRequired()]) # changed TextField to StringField
    # Region Of Interest
    roi = SelectField('Region of Interest', [DataRequired()],
    choices=[
        ('sq','100µm on 100µm square'),
        ('70µmsq', '70µm on 70µm square'),
        ('polygon','custom polygon'),
        ('none', 'full image')])
    
    # Width image µm
    widthm = StringField("Enter the width (in µm) here", validators=[validators.InputRequired()]) # changed TextField to StringField
    
    # Width image pixels
    widthpx = StringField("Enter the width (in pixels) here", validators=[validators.InputRequired()]) # changed TextField to StringField
    
    # # Screen resolution
    resolution = StringField(validators=[validators.InputRequired()], id='txtres')

    # Count tracks and review manually
    mineral = SelectField('mineral', [DataRequired()],
        choices=[
            ('please make a choice','please make a choice'),
            ('laft','apatite'),
            ('glass','mica'),
            ('annotate', 'annotate tracks for DNN development')])
    # Add type of microscope
    ms = StringField("Enter the type of microscope (optional)", default="")

    # DNN apatite
    dnnap = SelectField('DNN apatite', [DataRequired()],
        choices=[
            ('ap','apatite Nikon Gent 2020')])

    # DNN mica
    dnnmica = SelectField('DNN mica', [DataRequired()],
        choices=[
            ('mica','mica Nikon Gent 2020')])

    # Coordinates polygon
    polygoncoords = StringField(id = 'txtpolygoncoords')

    # Submit button
    #submit = SubmitField("Start automatic track recognition")

#--------------------------------------------------------------------------------------------
# -----------------------------------ROUTING------------------------------------------------- 
# -------------------------------------------------------------------------------------------
# Home page
@app.route("/")
def home():
    form_settings = SettingsForm(request.form)
    return render_template('home.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/download")
def download():
    return render_template('download.html')

@app.route("/setsettings", methods=['GET', 'POST'])
def setsettings():
    # Create form
    form_settings = SettingsForm(request.form)
     
    # Send template information to index.html
    return render_template('setsettings.html', title='Settings', form=form_settings)

@app.route("/dnndev", methods=['GET', 'POST'])
def dnndev():    
    # Send template information
    return render_template('dnndev.html')

@app.route("/dparsettings", methods=['GET', 'POST'])
def startdpar():
    # Create form
    form_settings_dpar=SettingsDpar(request.form)

    # Send template information
    return render_template('dparsettings.html',title='Settings', dparform=form_settings_dpar)

@app.route("/termsofuse")
def termsofuse():     
    return render_template('termsofuse.html')
    
@app.route("/frequentlyaskedquestions")
def faq():     
    return render_template('frequentlyaskedquestions.html')

# Get path. This information is needed for the uploads function (uploadspath). 
import paths 
import os

path = os.path.dirname(os.path.abspath( __file__ ))
uploadspath = os.path.join(path, paths.UPLOAD_DIR)

logging.info('Uploadpath is set to: '+uploadspath)

@app.route('/uploads/<filename>')
def send_file(filename):
    logging.info('send file executed')
    return send_from_directory(uploadspath, filename)

@app.route('/show/<filename>')
def uploaded_file(filename):
    logging.info('uploaded file executed')
    return render_template('aitracktiveannotate.html', filename=filename)

    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


#--------------------------------------------------------------------------------------------
# ----------------------------------AI-Track-tive starts here-------------------------------- 
# -------------------------------------------------------------------------------------------

from flask import Flask, Response
from werkzeug.utils import secure_filename
import datetime as dt
import numpy as np
from datetime import datetime
import io
from io import StringIO
from io import BytesIO
from werkzeug.wrappers import Response
from flask import send_file
from PIL import Image
import csv

# route http posts to this method
@app.route('/aitracktive', methods=['GET','POST'])
def main():

    logging.info('logging is successfully')

    from flask import Flask, render_template, request, flash
    from flask_mysql_connector import MySQL
    from werkzeug.wrappers import Response

    if request.method =='GET': # happens when I click on continue
        
        from flask import Flask, render_template, request
        from flask_mysql_connector import MySQL
        from werkzeug.wrappers import Response
        logging.info('get request occurred')
        return 
    
    elif request.method =='POST': # happens when I click on the submit button
        logging.info('Post request in aitracktive now. Try to read fetch data')

        #--------------------------------------------------------------------------------------------
        # ---------------------------------------- GET PATHS ---------------------------------------- 
        # -------------------------------------------------------------------------------------------
        
        # Get IP address
        logging.info('ip address comes below') 
        from flask import request
        ip_address = request.remote_addr
        logging.info(ip_address)

        # Create path
        import paths #refers to paths.py file 
        import os 

        path = os.path.dirname(os.path.abspath( __file__ ))
        uploadspath = os.path.join(path, paths.UPLOAD_DIR)
        
        #--------------------------------------------------------------------------------------------
        # ----------------------Connect to database and send info to database------------------------ 
        # -------------------------------------------------------------------------------------------       
        from flask import Flask, render_template, request
        from flask_mysql_connector import MySQL
        from werkzeug.wrappers import Response
        import os
        
        logging.info(' ')
        logging.info('START AITRACKTIVE')
        logging.info(' ')

        # Get settings from form 
        roi = request.form['roi']
        mineral = request.form['mineral']
        widthm = request.form['widthm']
        logging.info('widthm is '+str(widthm))
        widthpx = request.form['widthpx']
        customname = request.form['name']
        ms = request.form['ms']
        resolution = request.form['resolution']
        polygoncoords = request.form['polygoncoords']
        logging.info('polygoncoords')
        logging.info(polygoncoords)

        app = Flask(__name__)
        import storage
        conn = storage.connect()

        # Create app
        mysql = MySQL(app)

        # Using the connection property
        cur = conn.cursor()

        # Get a unique file name
        date = dt.datetime.now()
        datestamp = str(date)
        datestamp = datestamp.replace(" ", "_") # get crazy characters out of the name
        datestamp = datestamp.replace(".", "_") # get crazy characters out of the name
        datestamp = datestamp.replace(":", "_") # get crazy characters out of the name
        datestamp = datestamp.replace(";", "_") # get crazy characters out of the name
        datestamp = datestamp.replace("/", "_") # get crazy characters out of the name

        # Get the obligatory filenames
        picr = request.files['pic']
        logging.info('picr is'+str(picr))
        filename = str(str(datestamp) + '_AP_' + secure_filename(picr.filename))
        micar = request.files['mica']
        filename_mica = str(str(datestamp) + '_MICA_' + secure_filename(micar.filename))

        # If there was no custom name given, give an error
        if customname =='':
            logging.error('no name was given!')
            flash('no name was given!')
            session['validation_error'] = 'An error occurred: no name was inserted'
            return render_template('error.html')

        # If there was no resolution given, give an error
        if resolution =='':
            logging.error('no resolution was given!')
            session['validation_error'] = 'An error occurred: no resolution was inserted'
            return render_template('error.html')

        # If there was a polygonal mask chosen, and the user forgot to draw a polygon, give an error
        if roi =='polygon' and polygoncoords == '':
            logging.error('no coordinates for the polygon were given!')
            session['validation_error'] = 'An error occurred: no coordinates for the polygon were chosen'
            return render_template('error.html')

        # If there was no roi chosen
        if mineral == 'please make a choice':
            logging.error('no mineral was specified')
            session['validation_error'] = 'An error occurred: no mineral was specified'
            return render_template('error.html')

        # If there was no width given
        if widthm == '':
            logging.error('no width (in µm) was specified')
            session['validation_error'] = 'An error occurred: no width (in µm) was specified'
            return render_template('error.html')

        # Check if we can make a float from widthm input
        try:
            widthm = float(widthm)
        except:
            logging.error('input widthm is not a float or int')
            session['validation_error'] = 'An error occurred: width in micrometer is not a number like e.g. 105 or 101.5. Please reshape your input variable.'
            return render_template('error.html')

        # Check if we can make a float from widthm input
        try:
            widthpx = float(widthpx)
        except:
            logging.error('input widtpx is not a float or int')
            session['validation_error'] = 'An error occurred: width in pixels is not a number like e.g. 105 or 101.5. Please reshape your input variable.'
            return render_template('error.html')

        # If there was no width given
        if widthpx == '':
            logging.error('no width (px) was specified')
            session['validation_error'] = 'An error occurred: no width (in pixels) was specified'
            return render_template('error.html')

        # If no images were given, give an error
        if request.files['pic'].filename == '' and request.files['mica'].filename == '':
            logging.error('no image was given!')
            session['validation_error'] = 'An error occurred: for this method we need at least 1 jpg file'
            return render_template('error.html')


        # Get filetype
        mimetype_pic = picr.mimetype
        mimetype_mica = micar.mimetype



        # Get filetype after checking if there are images given
        if request.files['picz'].filename !='':
            piczr = request.files['picz']
            mimetype_picz = piczr.mimetype
            filenamez = str(str(datestamp) + '_AP_Z_' + secure_filename(picr.filename))
        else:
            mimetype_picz = picr.mimetype
            filenamez = filename

        if request.files['pic_epi'].filename !='':
            pic_epir = request.files['pic_epi']
            mimetype_pic_epi = pic_epir.mimetype
            filenameepi = str(str(datestamp) + '_AP_EPI_' + secure_filename(picr.filename))
        else:
            mimetype_pic_epi = picr.mimetype
            filenameepi = filename

        if request.files['micaz'].filename !='':
            micazr = request.files['micaz']
            mimetype_micaz = micazr.mimetype
            filename_micaz = str(str(datestamp) + '_MICA_Z_' + secure_filename(micar.filename))
        else:
            mimetype_micaz = micar.mimetype
            filename_micaz = filename_mica

        if request.files['mica_epi'].filename != '':
            mica_epir = request.files['mica_epi']
            filename_mica_epi = str(str(datestamp) + '_MICA_EPI_' + secure_filename(micar.filename))
            mimetype_mica_epi = mica_epir.mimetype
        else:
            mimetype_mica_epi = micar.mimetype
            filename_mica_epi = filename_mica

        #--------------------------------------------------------------------------------------------
        # ---------------------- Check if the images are all jpeg ------------------------ 
        # -------------------------------------------------------------------------------------------

        if mineral == 'laft':
            if mimetype_pic == 'image/jpeg' and mimetype_picz == 'image/jpeg' and mimetype_pic_epi == 'image/jpeg':
                logging.info('input is jpeg')
            else:
                session['validation_error'] = 'An error occurred: for this method we need 1 jpg file. You can find some information on this link https://www.aivia-software.com/post/imagej-fiji-quick-tip-1-convert-images-as-a-batch . There you can read how to use ImageJ to convert for example tiff files to jpeg'
                return render_template('error.html')

        elif mineral == 'glass':
            if mimetype_mica == 'image/jpeg' and mimetype_micaz =='image/jpeg' and mimetype_mica_epi =='image/jpeg':
                logging.info('input is jpeg')
            else:
                session['validation_error'] = 'An error occurred: for this method we need 1 jpg file'
                return render_template('error.html')

        elif mineral == 'anotate':
            if mimetype_pic == 'image/jpeg' and mimetype_picz == 'image/jpeg' and mimetype_pic_epi == 'image/jpeg' and mimetype_mica == 'image/jpeg' and mimetype_micaz =='image/jpeg'and mimetype_mica_epi =='image/jpeg':
                logging.info('input is jpeg')
            else:
                session['validation_error'] = 'An error occurred: for this method we need 1 jpg file'
                return render_template('error.html')

        logging.info('images are all jpegs')
        
        #--------------------------------------------------------------------------------------------
        # ------------------------Import functions that I'll need later------------------------------ 
        # -------------------------------------------------------------------------------------------
               
        def labelImgformatter(rectangles):
            # Every .txt starts with a 15 and space
            s = ''

            for r in rectangles:
                if float(r[1]) > 0:

                    r_converted = str('') # make an empty to string to append the values to
                    for value in r:
                        value = float(value)
                        r_converted += str('15 ')+str(abs(value))
                    s+=str(r_converted)+str('\n')
                else:
                    logging.info('negative')
            # Return output
            return s

        # Create a function that calculates the area of the polygon 
        def PolygonArea(corners,width):
            n = len(corners) # of corners
            logging.info('number of corners is '+str(n))
            logging.info(corners)

            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += corners[i][0] * corners[j][1]
                area -= corners[j][0] * corners[i][1]
            
            logging.info('area is '+str(area))

            area_pix = abs(area) / 2.0
            logging.info('area_pix is ' + str(area_pix))
            logging.info('widthimage is ' +str(width))
            logging.info('widthm is '+ str(widthm))
            converter=float(width)/float(widthm) # pix/µm

            logging.info('converter is ' + str(converter))
            
            area_µm=area_pix/(converter*converter)
            logging.info(str(area_µm) + 'µm²')
            
            return area_µm
        
        # Get resolution 
        logging.info('resolution parameters:')
        logging.info(resolution)
        resolution_split = resolution.split('*') 
        logging.info(resolution_split)
        screen_width = resolution_split[0]
        screen_width = int(screen_width)
        logging.info(screen_width)
        screen_height = resolution_split[1]
        screen_height = int(screen_height)
        logging.info(screen_height)

        #--------------------------------------------------------------------------------------------
        # ----------------------------------Start finding tracks------------------------------------- 
        # -------------------------------------------------------------------------------------------

        if mineral == 'laft':                
            CANVAS_SIZE = (800,800)
            FINAL_LINE_COLOR = (255, 255, 255) 
            WORKING_LINE_COLOR = (1,1,1)
            
            # Fission track recognition in apatite
            logging.info("Start of the apatite fission track recognition")

            # Read deep neural network and configuration file for apatite fission track recognition
            cwd = os.path.dirname(os.path.abspath( __file__ ))
            #cwd = os.path.dirname(os.path.realpath(__file__))
                        
            ann =  os.path.join(cwd, 'yolov3_apatite_Nikon_Gent_3000it_50img_December2020.weights')
            #os.path.join(path, "yolov3_apatite_Nikon_Gent_3000it_50img_December2020.weights")
            logging.info(ann)
            
            testnn = os.path.join(cwd, 'yolov3_testing.cfg')
            #os.path.join(path,"yolov3_testing.cfg")
            logging.info(testnn)
                
            net = cv2.dnn.readNet(ann, testnn)    
            #net = cv2.dnn.readNet("yolov3_apatite_Nikon_Gent_3000it_50img_December2020", "yolov3_testing.cfg") #old 
            
            # Get layer names
            layer_names = net.getLayerNames() 
            
            # Name custom object
            classes = ["Track"]         
            
            # Images path
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            colors = np.random.uniform(0, 255, size=(len(classes), 3))

            #--------------------------------------------------------------------------------------------
            # ----------------------------------Save images locally-------------------------------------- 
            # -------------------------------------------------------------------------------------------
            
            # Apatite img: if there is an image given
            if request.files['pic'].filename != '':
                apimg = Image.open(request.files['pic'].stream)
                npapimg = np.array(apimg)
                apimage = npapimg.copy() 
                apimage = cv2.cvtColor(apimage,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = apimage.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                apimage = cv2.resize(apimage, None, fx=f, fy=f) 
                height, width, channels = apimage.shape
                apimage_orig = apimage

                location = os.path.join(uploadspath,filename)
                cv2.imwrite(location,apimage) 

                # Save copy
                filenamecopy = str(str(datestamp) + '_AP_COPY_' + secure_filename(picr.filename))
                location = os.path.join(uploadspath,filenamecopy)
                cv2.imwrite(location,apimage) 
            else:
                logging.info(request.files['pic'].filename)

            # Apatite imgz: if there is an image given
            if request.files['picz'].filename != '':
                apimgz = Image.open(request.files['picz'].stream)
                npapimgz = np.array(apimgz)
                apimagez = npapimgz.copy() 
                apimagez = cv2.cvtColor(apimagez,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = apimagez.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                apimagez = cv2.resize(apimagez, None, fx=f, fy=f) 
                height, width, channels = apimagez.shape
                location = os.path.join(uploadspath,filenamez)
                cv2.imwrite(location,apimagez) 

            # Apatite imgz: if there is an image given
            if request.files['pic_epi'].filename != '':
                apimgepi = Image.open(request.files['pic_epi'].stream)
                npapimgepi = np.array(apimgepi)
                apimageepi = npapimgepi.copy() 
                apimageepi = cv2.cvtColor(apimageepi,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = apimageepi.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                apimageepi = cv2.resize(apimageepi, None, fx=f, fy=f) 
                height, width, channels = apimageepi.shape
                location = os.path.join(uploadspath,filenameepi)
                cv2.imwrite(location,apimageepi) 
                        
            # Scaling: find parameters for a 100 µm on 100 µm window to slice the photo's
            px = float(widthpx)*f
            dist = float(widthm)
            s1 = round(0.5*(px-(px*100)/dist))
            logging.info('s1 is '+str(s1))
            s2 = round(float(px) - float(s1)) 
            logging.info('s2 is '+str(s2))

            # Scaling: find parameters for a 70 µm on 70 µm window to slice the photo's
            s3 = round(0.5*(px-(px*70)/dist))
            logging.info('s3 is '+str(s3))
            s4 = round(float(px) - float(s3)) 
            logging.info('s4 is '+str(s4))

            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Region of interest-------------------------------------- 
            # -------------------------------------------------------------------------------------------
            
            # Draw a polygonal graticule if the polygon is not predefined
            if roi == 'polygon':

                polygoncoords = polygoncoords.split(',')
                polygoncoordslist = list()
                # Get list of strings
                for i in polygoncoords:
                    i = i.replace('[','')
                    i = i.replace(']','')
                    polygoncoordslist.append(i)

                l = len(polygoncoordslist)

                halfl = int(l*0.5)
                logging.info('polygoncoordslist')
                logging.info(polygoncoordslist)

                polygoncoordslist2=list()
                # Get list of tuples
                for j in range(halfl):
                    i_1 = int(2*j) 
                    i_2 = int(i_1 + 1)
                    # it is necessary to rescale the polygons using the resizing parameter f
                    c_1 = round(float(polygoncoordslist[i_1])*f)  
                    # it is necessary to rescale the polygons using the resizing parameter f
                    c_2 = round(float(polygoncoordslist[i_2])*f)  
                    c = tuple([c_1,c_2])
                    logging.info(c)
                    polygoncoordslist2.append(c)
                
                # Show the coordinates
                logging.info('polygoncoordslist2')
                logging.info(polygoncoordslist2)            

                # Make mask
                mask = np.full_like(apimage,(0,0,0)) 
                cv2.fillPoly(mask, np.array([polygoncoordslist2]), FINAL_LINE_COLOR)  

                # extra step: see https://pythonprogramming.net/lane-region-of-interest-python-plays-gta-v/
                mask_flipped = cv2.bitwise_and(apimage, mask)   #this operation flips the bits
                
                croppedimage = mask_flipped
                
                # Calculate area of polygon
                area = PolygonArea(polygoncoordslist2,width)
                polygon_output = polygoncoordslist2
                        
            elif roi == 'sq':

                # Calculate area of polygon
                mask = np.full_like(apimage,(0,0,0))        
                
                polygon_points_square = [(s1,s1),(s2,s1),(s2,s2),(s1,s2)]
                logging.info('type of polygon_points_square')
                logging.info(type(polygon_points_square))

                area = PolygonArea(polygon_points_square, width)
                logging.info("polygon points square")
                logging.info(polygon_points_square)

                cv2.fillPoly(mask, np.array([polygon_points_square]), FINAL_LINE_COLOR)  

                # extra step: see https://pythonprogramming.net/lane-region-of-interest-python-plays-gta-v/
                #this operation flips the bits
                mask_flipped = cv2.bitwise_and(apimage, mask)   
                croppedimage = mask_flipped

                polygon_output = polygon_points_square

            elif roi == '70µmsq':

                # Calculate area of polygon
                mask = np.full_like(apimage,(0,0,0))        
                
                polygon_points_square = [(s3,s3),(s4,s3),(s4,s4),(s3,s4)]
                logging.info('type of polygon_points_square')

                area = PolygonArea(polygon_points_square, width)
                logging.info("polygon points square")

                cv2.fillPoly(mask, np.array([polygon_points_square]), FINAL_LINE_COLOR)  

                # extra step: see https://pythonprogramming.net/lane-region-of-interest-python-plays-gta-v/
                #this operation flips the bits
                mask_flipped = cv2.bitwise_and(apimage, mask)  
                croppedimage = mask_flipped
                polygon_output = polygon_points_square

            # If the full field of view needs to be shown
            elif roi == 'none':
                logging.info('roi: full image ')
                polygon_points=[(0,0),(int(width),0),(int(width),int(width)),(0,int(width))]
                croppedimage = apimage_orig  
                
                # Calculate area of polygon
                area = PolygonArea(polygon_points, width)
                polygon_output = polygon_points
            else:
                logging.info('the type of graticule was not specified!')

            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Detect objects ----------------------------------------- 
            # -------------------------------------------------------------------------------------------

            blob = cv2.dnn.blobFromImage(apimage_orig, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # same as default
            net.setInput(blob)
            outs = net.forward(output_layers)
            
            # Make some new lists to add stuff
            class_ids = []
            confidences = []
            boxes = []

            # Convert to grayscale object
            gray_version_apatite = cv2.cvtColor(croppedimage, cv2.COLOR_RGB2GRAY)
        
            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Apatite fission track: rectangle drawing----------------
            # -------------------------------------------------------------------------------------------

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.1: #default is 0.3, now it is 0.1 which means that every track with 10% confidence is picked

                        #logging.info('rectangle drawing: not none')
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                    
                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
            
                        # Develop an if-else structure that erases the found tracks covered by the polygon
                        if np.any(gray_version_apatite[center_y,center_x]) == 0:
                            if np.any(gray_version_apatite[y,x]) == 0:
                                pass
                            else:
                                pass

                        else:
                            # both are not in black
                            if np.any(gray_version_apatite[y,x]) != 0:
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                            
                            # center is not in black , edge is in black
                            else:
                                #logging.info('else')
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                        
            logging.info('len boxes is '+str(len(boxes)))
                
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.6)  # 0.5 and 0.4 resp originally. 
            # But I tweeked it to have better results for the application for which we use it
            # If you tweak the first value (behind confidences), you change the identification treshokld (confidence if I remember well, see opencv2 website)
            # If you raise the second value, you better detect the overlapping tracks 
            
            # Determine font
            font2 = cv2.FONT_HERSHEY_PLAIN
            
            # Make list to store the rectangles for LabelImgFormatter function 
            rect_txt_list_ap = list()
            
            # Draw rectangles for every detected track  
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    color = colors[class_ids[i]]
                    color_text=(1,1,0)
                    cv2.rectangle(croppedimage, (x, y), (x + w, y + h), (200,0,0), 1)
                    
                    # Txt file needs fractions
                    rect_txt = list()
                    x_txt = str((0.5*w + x)/(width))
                    rect_txt.append(x_txt[:8])
                    y_txt = str((0.5*w + y)/width)
                    rect_txt.append(y_txt[:8])
                    w_txt = str(w/width)
                    rect_txt.append(w_txt[:8])
                    h_txt = str(h/width)
                    rect_txt.append((h_txt[:8]))
                    
                    # Append the self-identified rectangle to the list 
                    rect_txt_list_ap.append(rect_txt)
                    
            # produce the .txt file
            logging.info('first five from rect txt list ap') 
            logging.info(rect_txt_list_ap[0:5])
            labelimg_string = labelImgformatter(rect_txt_list_ap)
            logging.info('first 50 signs from labelimgstring')
            logging.info(labelimg_string[0:50])            
            
            #Executing SQL Statements 
            sql = "INSERT INTO img (customname,name,method,regionofinterest,widthm,widthpx,date,resolution,ms,ip,labelimg_auto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
            val = (str(customname),str(filename),str(mineral),str(roi),str(widthm),str(widthpx),str(date),str(screen_height),str(ms),str(ip_address), str(labelimg_string)) 
            cur.execute(sql,val)

            # Saving the actions performed on the database
            conn.commit()
            
            # Save image locally
            location = os.path.join(uploadspath,filename)
            logging.info(location)
            cv2.imwrite(location,croppedimage)
            logging.info('imwrite')

            # Variables
            polygon = polygon_output
            stp = len(boxes) # spontaneous true positives
            sfn = 'tbfi' # spontaneous false negatives
            sfp = 'tbfi' # spontaneous false positives
            ns = 'tbfi'
            itp = 'n/a' # induced true positives
            ifn = 'n/a' # induced false negatives
            ifp = 'n/a' # induced false positives 
            ni = 'n/a'
            rhosroi = 'n/a'
            dnnap = "yolov3_apatite_Nikon_Gent_3000it_50img_December2020.weights" # deep neural network apatite
            dnnmica = 'n/a' # deep neural network mica 
            stp_indexes = ...
          
            # Export data as .csv file when finished
            from datetime import datetime
            import pandas as pd

            # Make dictionary with names and values
            d = {'Name': ['Method', 'Name apatite', 'Name mica', 'Area', 'Ns', 'Ni', 'Polygon', 'Spont tracks: true positives', 'Spont tracks: false negatives', 'Spont tracks: false positives', 'Induced tracks: true positives' , 'Induced tracks: false negatives', 'Induced tracks: false positives', 'DNN apatite', 'DNN mica', 'apprecision', 'aprecall', 'micaprecision', 'micarecall'], 
                'Value': ['Apatite',filename, 'n/a', area, ns, ni, polygon, stp, sfn, sfp, itp, ifn, ifp, dnnap, dnnmica, 'apprecision', 'aprecall', 'n/a', 'n/a'],
                }

            # Export to a panda dataframe
            df = pd.DataFrame(data=d)
            
            # Get name of the csv file 
            name_csv = str(str(filename[:-4])+'.csv')
            logging.info('send from directory')
            logging.info(name_csv)

            # Make csv file from panda
            df.to_csv(os.path.join(uploadspath,name_csv))
            
            # Return to the annotation window 
            logging.info('render template')
            return render_template('aitracktiveannotate.html', filename = filename, filenamez = filenamez, filenameepi = filenameepi, mineral = mineral)

        #----------------------------------------------------------------------------------------
        # ---------------------------------- Mica now ------------------------------------------- 
        # ---------------------------------------------------------------------------------------

        # If only mica needs to be analyzed
        elif mineral == 'glass':
         
            CANVAS_SIZE = (800,800)
            FINAL_LINE_COLOR = (255, 255, 255) 
            WORKING_LINE_COLOR = (1,1,1)
            
            # Fission track recognition in mica
            logging.info("Start of the mica fission track recognition")

            # Read deep neural network and configuration file for apatite fission track recognition            
            cwd = os.path.dirname(os.path.abspath( __file__ ))
            #cwd = os.path.dirname(os.path.realpath(__file__))
                        
            ann =  os.path.join(cwd, 'yolov3_apatite_Nikon_Gent_3000it_50img_December2020.weights')
            logging.info(ann)
            
            testnn = os.path.join(cwd, 'yolov3_testing.cfg')
            logging.info(testnn)
                
            net = cv2.dnn.readNet(ann, testnn)    

            # Get layer names
            layer_names = net.getLayerNames() 
            
            # Name custom object
            classes = ["Track"]         
            
            # Images path
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            colors = np.random.uniform(0, 255, size=(len(classes), 3))

            #--------------------------------------------------------------------------------------------
            # ----------------------------------Save images locally-------------------------------------- 
            # -------------------------------------------------------------------------------------------
            
            # Mica img: if there is an image given
            if request.files['mica'].filename != '':
                micaimg = Image.open(request.files['mica'].stream)
                npmicaimg = np.array(micaimg)
                micaimage = npmicaimg.copy() 
                micaimage = cv2.cvtColor(micaimage,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = micaimage.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                micaimage = cv2.resize(micaimage, None, fx=f, fy=f) 
                height, width, channels = micaimage.shape
                micaimage_orig = micaimage

                location = os.path.join(uploadspath,filename_mica)
                logging.info('location is ...')
                logging.info(location)
                cv2.imwrite(location,micaimage) 

                # Save copy
                filenamecopy = str(str(datestamp) + '_MICA_COPY_' + secure_filename(micar.filename))
                location = os.path.join(uploadspath,filenamecopy)
                cv2.imwrite(location,micaimage) 
            
            # Mica imgz: if there is an image given
            if request.files['micaz'].filename != '':
                micaimgz = Image.open(request.files['micaz'].stream)
                npmicaimgz = np.array(micaimgz)
                micaimagez = npmicaimgz.copy() 
                micaimagez = cv2.cvtColor(micaimagez,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = micaimagez.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                micaimagez = cv2.resize(micaimagez, None, fx=f, fy=f) 
                height, width, channels = micaimagez.shape
                location = os.path.join(uploadspath,filename_micaz)
                logging.info('location')
                logging.info(location)
                logging.info('filename_micaz')
                logging.info(filename_micaz)
                cv2.imwrite(location,micaimagez) 

            # Mica img epi: if there is an image given
            if request.files['mica_epi'].filename != '':
                micaimgepi = Image.open(request.files['mica_epi'].stream)
                npmicaimgepi = np.array(micaimgepi)
                micaimageepi = npmicaimgepi.copy() 
                micaimageepi = cv2.cvtColor(micaimageepi,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = micaimageepi.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                micaimageepi = cv2.resize(micaimageepi, None, fx=f, fy=f) 
                height, width, channels = micaimageepi.shape
                location = os.path.join(uploadspath,filename_mica_epi)
                cv2.imwrite(location,micaimageepi) 
                        
            # Scaling: find parameters for a 100 µm on 100 µm window to slice the photo's
            px = float(widthpx)*f
            dist = float(widthm)
            s1 = round(0.5*(px-(px*100)/dist))
            logging.info('s1 is '+str(s1))
            s2 = round(float(px) - float(s1)) 
            logging.info('s2 is '+str(s2))

            # Scaling: find parameters for a 70 µm on 70 µm window to slice the photo's
            s3 = round(0.5*(px-(px*70)/dist))
            logging.info('s3 is '+str(s3))
            s4 = round(float(px) - float(s3)) 
            logging.info('s4 is '+str(s4))

            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Region of interest-------------------------------------- 
            # -------------------------------------------------------------------------------------------
            
            # Draw a polygonal graticule if the polygon is not predefined
            if roi == 'polygon':

                polygoncoords = polygoncoords.split(',')
                polygoncoordslist = list()
                # Get list of strings
                for i in polygoncoords:
                    i = i.replace('[','')
                    i = i.replace(']','')
                    polygoncoordslist.append(i)

                l = len(polygoncoordslist)

                halfl = int(l*0.5)

                polygoncoordslist2=list()
                # Get list of tuples
                for j in range(halfl):
                    i_1 = int(2*j) 
                    i_2 = int(i_1 + 1)
                    # it is necessary to rescale the polygons using the resizing parameter f
                    c_1 = round(float(polygoncoordslist[i_1])*f) 
                    # it is necessary to rescale the polygons using the resizing parameter f
                    c_2 = round(float(polygoncoordslist[i_2])*f) 
                    c = tuple([c_1,c_2])
                    logging.info(c)
                    polygoncoordslist2.append(c)
                
                
                logging.info(polygoncoordslist2)
                p = np.array(polygoncoordslist2)
                logging.info(p)

                # Make mask
                mask = np.full_like(micaimage,(0,0,0)) 
                cv2.fillPoly(mask, np.array([polygoncoordslist2]), FINAL_LINE_COLOR)  

                # extra step: see https://pythonprogramming.net/lane-region-of-interest-python-plays-gta-v/
                 #this operation flips the bits
                mask_flipped = cv2.bitwise_and(micaimage, mask)  
                
                # Get area
                area = PolygonArea(polygoncoordslist2, width)

                croppedimage = mask_flipped
                
                # Calculate area of polygon
                area = PolygonArea(polygoncoordslist2,width)
                polygon_output = polygoncoordslist2
                        
            elif roi == 'sq':

                # Calculate area of polygon
                mask = np.full_like(micaimage,(0,0,0))        
                
                polygon_points_square = [(s1,s1),(s2,s1),(s2,s2),(s1,s2)]
                logging.info('type of polygon_points_square')
                logging.info(type(polygon_points_square))
                logging.info(type(polygon_points_square[0]))

                area = PolygonArea(polygon_points_square, width)
                logging.info("polygon points square")
                logging.info(polygon_points_square)

                cv2.fillPoly(mask, np.array([polygon_points_square]), FINAL_LINE_COLOR)  

                # extra step: see https://pythonprogramming.net/lane-region-of-interest-python-plays-gta-v/
                # this operation flips the bits
                mask_flipped = cv2.bitwise_and(micaimage, mask)  
                croppedimage = mask_flipped

                polygon_output = polygon_points_square

            elif roi == '70µmsq':

                # Calculate area of polygon
                mask = np.full_like(micaimage,(0,0,0))        
                logging.info('s3 is'+str(s3))                
                logging.info('s4 is'+str(s4))

                polygon_points_square = [(s3,s3),(s4,s3),(s4,s4),(s3,s4)]
                logging.info('type of polygon_points_square')
                logging.info(type(polygon_points_square))
                logging.info(type(polygon_points_square[0]))

                area = PolygonArea(polygon_points_square, width)
                logging.info("polygon points square")
                logging.info(polygon_points_square)

                cv2.fillPoly(mask, np.array([polygon_points_square]), FINAL_LINE_COLOR)  

                # extra step: see https://pythonprogramming.net/lane-region-of-interest-python-plays-gta-v/
                mask_flipped = cv2.bitwise_and(micaimage, mask)   #this operation flips the bits
                croppedimage = mask_flipped

                polygon_output = polygon_points_square

            # If the full field of view needs to be shown
            elif roi == 'none':
                logging.info('roi: full image ')
                polygon_points=[(0,0),(int(width),0),(int(width),int(width)),(0,int(width))]
                croppedimage = micaimage_orig  
                
                # Calculate area of polygon
                area = PolygonArea(polygon_points, width)
                polygon_output = polygon_points
            else:
                logging.info('the type of graticule was not specified!')

            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Detect objects ----------------------------------------- 
            # -------------------------------------------------------------------------------------------

            blob = cv2.dnn.blobFromImage(micaimage_orig, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # same as default
            net.setInput(blob)
            outs = net.forward(output_layers)
            
            # Make some new lists to add stuff
            class_ids = []
            confidences = []
            boxes = []
            logging.info('len boxes is '+str(len(boxes)))

            # Convert to grayscale object
            gray_version_mica = cv2.cvtColor(croppedimage, cv2.COLOR_RGB2GRAY)
        
            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Mica fission track: rectangle drawing----------------
            # -------------------------------------------------------------------------------------------

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    #default confidence value is 0.3, now it is 0.1 which means that every track with 10% confidence is picked
                    if confidence > 0.1: 

                        #logging.info('rectangle drawing: not none')
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                    
                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
            
                        # Develop an if-else structure that erases the found tracks covered by the polygon
                        if np.any(gray_version_mica[center_y,center_x]) == 0:
                            if np.any(gray_version_mica[y,x]) == 0:
                                pass
                            else:
                                pass

                        else:
                            # both are not in black
                            if np.any(gray_version_mica[y,x]) != 0:
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                            
                            # center is not in black , edge is in black
                            else:
                                #logging.info('else')
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                        
            logging.info('len boxes is '+str(len(boxes)))
                
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.01, 0.6)  # 0.5 and 0.4 resp originally. 
            # But I tweeked it to have better results for the application for which we use it
            # If you tweak the first value (behind confidences), you change the identification treshokld (confidence if I remember well, see opencv2 website)
            # If you raise the second value, you better detect the overlapping tracks 
            
            # Determine font
            font2 = cv2.FONT_HERSHEY_PLAIN
            
            # Make list to store the rectangles for LabelImgFormatter function 
            rect_txt_list_mica = list()
            
            # Draw rectangles for every detected track  
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    color = colors[class_ids[i]]
                    color_text=(1,1,0)
                    cv2.rectangle(croppedimage, (x, y), (x + w, y + h), (200,0,0), 1)
                    
                    # Txt file needs fractions
                    rect_txt = list()
                    x_txt = str((0.5*w + x)/(width))
                    rect_txt.append(x_txt[:8])
                    y_txt = str((0.5*w + y)/width)
                    rect_txt.append(y_txt[:8])
                    w_txt = str(w/width)
                    rect_txt.append(w_txt[:8])
                    h_txt = str(h/width)
                    rect_txt.append((h_txt[:8]))
                    
                    # Append the self-identified rectangle to the list 
                    rect_txt_list_mica.append(rect_txt)
                    
            # produce the .txt file 
            labelimg_string = labelImgformatter(rect_txt_list_mica)
            logging.info('labelimgstring')
            logging.info(labelimg_string[0:50])            
            
            #Executing SQL Statements 
            sql = "INSERT INTO img (customname,name,method,regionofinterest,widthm,widthpx,date,resolution,ms,ip,labelimg_auto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
            val = (str(customname),str(filename_mica),str(mineral),str(roi),str(widthm),str(widthpx),str(date),str(screen_height),str(ms),str(ip_address),str(labelimg_string)) 
            cur.execute(sql,val)

            # Saving the actions performed on the database
            conn.commit()
            
            # Save image locally
            location = os.path.join(uploadspath,filename_mica)
            logging.info(location)
            cv2.imwrite(location,croppedimage)
            logging.info('imwrite')

            # Variables
            polygon = polygon_output
            stp = 'n/a' # spontaneous true positives
            sfn = 'n/a' # spontaneous false negatives
            sfp = 'n/a' # spontaneous false positives
            ns = 'n/a'
            itp = len(boxes) # induced true positives
            ifn = 'tbfi' # induced false negatives
            ifp = 'tbfi' # induced false positives 
            ni = 'tbfi'
            rhosroi = 'n/a'
            dnnap = "n/a" # deep neural network apatite
            dnnmica = "yolov3_mica_Nikon_Gent_2000it_50img_December2020.weights" # deep neural network mica 
          
            # Export data as .csv file when finished
            from datetime import datetime
            import pandas as pd

            # Make dictionary with names and values
            d = {'Name': ['Method', 'Name apatite', 'Name mica', 'Area', 'Ns', 'Ni', 'Polygon', 'Spont tracks: true positives', 'Spont tracks: false negatives', 'Spont tracks: false positives', 'Induced tracks: true positives' , 'Induced tracks: false negatives', 'Induced tracks: false positives', 'DNN apatite', 'DNN mica', 'apprecision', 'aprecall', 'micaprecision', 'micarecall'], 
                'Value': ['Apatite','n/a', filename_mica, area, ns, ni, polygon, stp, sfn, sfp, itp, ifn, ifp, dnnap, dnnmica, 'apprecision', 'aprecall', 'n/a', 'n/a'],
                }

            # Export to a panda dataframe
            df = pd.DataFrame(data=d)
            
            # Get name of the csv file 
            name_csv = str(str(filename_mica[:-4])+'.csv')
            logging.info('send from directory')
            logging.info(name_csv)

            # Make csv file from panda
            df.to_csv(os.path.join(uploadspath,name_csv))
            
            # Return to the annotation window 
            logging.info('render template')
            return render_template('aitracktiveannotate.html', filename = filename_mica, filenamez = filename_micaz, filenameepi = filename_mica_epi, mineral = mineral)

        #----------------------------------------------------------------------------------------
        # ---------------------------------- Do annotation now-----------------------------------
        # ---------------------------------------------------------------------------------------

        elif mineral == 'annotate':
            
            # copy glass starts now
            CANVAS_SIZE = (800,800)
            FINAL_LINE_COLOR = (255, 255, 255) 
            WORKING_LINE_COLOR = (1,1,1)
            
            # Fission track recognition in mica
            logging.info("Start of the mica fission track recognition")
            
            # Name custom object
            classes = ["Track"]         

            # Check if there was a name given
            if customname =='':
                logging.info('no name was given!')
                session['validation_error'] = 'An error occurred: no name was inserted'
                return render_template('error.html')

            # Check if there were files given
            if request.files['pic'].filename == '' and request.files['mica'].filename == '':
                logging.info('no image was given!')
                session['validation_error'] = 'An error occurred: for this method we need 1 jpg file uploaded using the mica button'
                return render_template('error.html')

            # Check if an image was given for the annotation method
            if mineral =='annotate' and request.files['mica'].filename =='':
                logging.info('no picture was given!')
                session['validation_error'] = 'An error occurred: you need to upload an image to the mica button in order to be able to make annotations (no matter what mineral it is)'
                return render_template('error.html')

            #--------------------------------------------------------------------------------------------
            # ----------------------------------Save images locally-------------------------------------- 
            # -------------------------------------------------------------------------------------------
            
            # Mica img: if there is an image given
            if request.files['mica'].filename != '':
                micaimg = Image.open(request.files['mica'].stream)
                npmicaimg = np.array(micaimg)
                micaimage = npmicaimg.copy() 
                micaimage = cv2.cvtColor(micaimage,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = micaimage.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                micaimage = cv2.resize(micaimage, None, fx=f, fy=f) 
                height, width, channels = micaimage.shape
                micaimage_orig = micaimage

                location = os.path.join(uploadspath,filename_mica)
                logging.info('location is ...')
                logging.info(location)
                cv2.imwrite(location,micaimage) 

                # Save copy
                filenamecopy = str(str(datestamp) + '_MICA_COPY_' + secure_filename(micar.filename))
                location = os.path.join(uploadspath,filenamecopy)
                cv2.imwrite(location,micaimage) 
            
            # Mica imgz: if there is an image given
            if request.files['micaz'].filename != '':
                micaimgz = Image.open(request.files['micaz'].stream)
                npmicaimgz = np.array(micaimgz)
                micaimagez = npmicaimgz.copy() 
                micaimagez = cv2.cvtColor(micaimagez,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = micaimagez.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                micaimagez = cv2.resize(micaimagez, None, fx=f, fy=f) 
                height, width, channels = micaimagez.shape
                location = os.path.join(uploadspath,filename_micaz)
                logging.info('location')
                logging.info(location)
                logging.info('filename_micaz')
                logging.info(filename_micaz)
                cv2.imwrite(location,micaimagez) 

            # Mica img epi: if there is an image given
            if request.files['mica_epi'].filename != '':
                micaimgepi = Image.open(request.files['mica_epi'].stream)
                npmicaimgepi = np.array(micaimgepi)
                micaimageepi = npmicaimgepi.copy() 
                micaimageepi = cv2.cvtColor(micaimageepi,cv2.COLOR_BGR2RGB) #convert colors otherwise they are shifted
                height, width, channels = micaimageepi.shape 
                
                # Resizing  
                f = float(0.70*screen_height)/float(height)
                micaimageepi = cv2.resize(micaimageepi, None, fx=f, fy=f) 
                height, width, channels = micaimageepi.shape
                location = os.path.join(uploadspath,filename_mica_epi)
                cv2.imwrite(location,micaimageepi) 
                        
            # Scaling: find parameters for a 100 µm on 100 µm window to slice the photo's
            px = float(widthpx)*f
            dist = float(widthm)

            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Region of interest-------------------------------------- 
            # -------------------------------------------------------------------------------------------
            
            logging.info('roi: full image ')
            polygon_points=[(0,0),(int(width),0),(int(width),int(width)),(0,int(width))]
            croppedimage = micaimage_orig  
            
            # Calculate area of polygon
            area = PolygonArea(polygon_points, width)
            polygon_output = polygon_points

            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Upload to database-------------------------------------- 
            # -------------------------------------------------------------------------------------------
            
            import storage
            conn = storage.connect()
            cur = conn.cursor()

            # Send info to the database 
            sql = "INSERT INTO img (customname,name,method,regionofinterest,widthm,widthpx,date,resolution,ms,ip,labelimg_auto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
            val = (str(customname),str(filename_mica),str(mineral),str(roi),str(widthm),str(widthpx),str(date),str(screen_height),str(ms),str(ip_address), 'n/a') 
            cur.execute(sql,val)

            # Saving the actions performed on the database
            conn.commit()
            
            # Close the cursor
            cur.close()

            #--------------------------------------------------------------------------------------------
            # ---------------------------------- Detect objects ----------------------------------------- 
            # -------------------------------------------------------------------------------------------

            # Make some new lists to add stuff
            class_ids = []
            confidences = []
            boxes = []
            logging.info('len boxes is '+str(len(boxes)))
           
            # Save image locally
            location = os.path.join(uploadspath,filename_mica)
            logging.info(location)
            cv2.imwrite(location,croppedimage)
            logging.info('imwrite')

            # # Make dictionary with names and values
            d = {'Name': ['Method', 'Name', 'Induced: false negatives'], 
                 'Value': ['Annotate', filename, 'n/a'],
                 }

            # # Export to a panda dataframe
            import pandas as pd
            df = pd.DataFrame(data=d)
            
            # Get name of the csv file 
            name_csv = os.path.join(uploadspath,str(str(filename_mica[:-4])+'.csv'))
            logging.info('name_csv mica')
            logging.info(name_csv)

            # # Make csv file from panda
            df.to_csv(name_csv)
            
            # Return to the annotation window 
            logging.info('render template')
            filename_micaz = filename_mica #annotate
            filename_mica_epi = filename_mica #annotate
            return render_template('aitracktiveannotate.html', filename = filename_mica, filenamez = filename_micaz, filenameepi = filename_mica_epi, mineral = mineral)      
        
        else:
            return render_template('setsettings.html')

# Second route that gathers information from the manual annotatepage 
@app.route('/aitracktive2ndpage/<filename>', methods=['GET','POST'])
def aitracktive2ndpage(filename):
    logging.info('aitracktive 2nd page starts')
    from flask import Flask, render_template, request
    from flask_mysql_connector import MySQL
    from werkzeug.wrappers import Response

    if request.method =='GET': # happens when I click on continue
        logging.info('get request aitracktive2')

        browser = request.user_agent.browser
        logging.info('user agent (browser type):'+str(browser))

        # Get filenames
        import os
        logging.info(os.getcwd())
        os.chdir(uploadspath)
        logging.info(os.getcwd())
        
        filename_img = os.path.join(uploadspath, str(filename)) # try this
        filename_csv = os.path.join(uploadspath,str(filename[:-4]+'.csv'))
        filename_txt = os.path.join(uploadspath,str(filename[:-4]+'.txt'))
        # Get zip file
        files = [filename_img, filename_csv,filename_txt]

        logging.info('files are '+str(files))
        import zipfile
        import os

        zipf = zipfile.ZipFile(str(filename)+'.zip','w', zipfile.ZIP_DEFLATED)

        # Try to find the jpg file 
        try:
            logging.info('filename img is...')
            logging.info(filename_img)
            a = os.path.basename(filename_img)
            zipf.write(filename_img,a)
        except:
            logging.info('an exception has occured: the jpg file is not found')

        # Try to find the csv file: normally successful
        try:
            b = os.path.basename(filename_csv)
            zipf.write(filename_csv,b)
        except:
            logging.info('an exception has occured: the csv file is not found')

        # Try to find the txt file: gives an error normally
        try:
            c = os.path.basename(filename_txt)
            zipf.write(filename_txt,c)
        except:
            logging.info('an exception has occured: the txt file is not found')
        

        zipf.close()
        logging.info('zipfile closed')
        logging.info(zipf)

        filenamezip = os.path.join(uploadspath,filename)
        filenamezip = filenamezip+'.zip'
        logging.info('filenamezip')
        logging.info(filenamezip)

        return send_file(filenamezip,
                mimetype = 'application/zip',
                attachment_filename= filename+'.zip',
                as_attachment = True)
    
    elif request.method =='POST': # happens when I click on the button
        logging.info('Post request in aitracktive2 now. Try to read fetch data')

        # Import data
        data = request.get_json() # get dictionary
        logging.info('data is '+str(data))
        import os
        filename = data['name']
        mineral = data['mineral']
        width = data['width']        

        def labelImgformatter(rectangles):
            # Every .txt starts with a 15 and space
            s = ''
            for r in rectangles:
                if float(r[1]) > 0:

                    r_converted = str('') # make an empty to string to append the values to
                    for value in r:
                        value = float(value)
                        r_converted += str('15 ')+str(abs(value))
                    s+=str(r_converted)+str('\n')
                else:
                    logging.info('negative')
            
            # Return output
            return s 

        if mineral == 'laft':

            loc = os.path.join(uploadspath,filename)
            croppedimage = cv2.imread(loc) 
            logging.info('image read')

            # Make list to store the rectangles for LabelImgFormatter function
            rect_txt_list_ap_fn = list()
            rect_txt_list_ap_fp = list()

            # Get false negatives list
            false_negatives=data['coords_fn'] 
            logging.info('false negatives')
            logging.info(false_negatives)
            logging.info(len(false_negatives))

            # Get false positives list
            false_positives=data['coords_fp']
            logging.info('false positives')
            logging.info(false_positives)
            
            # False negatives: draw rectangles on image
            for i in range(len(false_negatives)):
                l = false_negatives[i]

                x = l['x']
                y = l['y']
                w = l['w']
                h = l['h']
                
                a = int(round(x))
                b = int(round(y ))
                c = int(round(x + w))
                d = int(round(y + h))

                cv2.rectangle(croppedimage, (a,b), (c,d), (0,200,0), 1)

                # Txt file needs fractions
                rect_txt = list()

                x_txt = str((0.5*w + x)/(width))
                rect_txt.append(x_txt[:8])
                y_txt = str((0.5*w + y)/width)
                rect_txt.append(y_txt[:8])
                w_txt = str(w/width)
                rect_txt.append(w_txt[:8])
                h_txt = str(h/width)
                rect_txt.append((h_txt[:8]))
                
                # Append the self-identified rectangle to the list 
                rect_txt_list_ap_fn.append(rect_txt)

            labelimg_fn = labelImgformatter(rect_txt_list_ap_fn)

            # False positives: draw rectangles on image
            for i in range(len(false_positives)):
                l = false_positives[i]

                x = l['x']
                y = l['y']
                w = l['w']
                h = l['h']
                
                a = int(round(x))
                b = int(round(y))
                c = int(round(x + w))
                d = int(round(y + h))

                cv2.rectangle(croppedimage, (a,b), (c,d), (0,0,200), 1)

                # Txt file needs fractions
                rect_txt = list()

                x_txt = str((0.5*w + x)/(width))
                rect_txt.append(x_txt[:8])
                y_txt = str((0.5*w + y)/width)
                rect_txt.append(y_txt[:8])
                w_txt = str(w/width)
                rect_txt.append(w_txt[:8])
                h_txt = str(h/width)
                rect_txt.append((h_txt[:8]))

                # Append the self-identified rectangle to the list 
                rect_txt_list_ap_fp.append(rect_txt)

            labelimg_fp = labelImgformatter(rect_txt_list_ap_fp)

            cv2.imwrite(loc,croppedimage)

            #==============================================================
            # IMPORT DATA FROM CSV FILE
            #==============================================================
            
            import pandas as pd
            # Read csv file 
            name_csv = os.path.join(uploadspath,str(str(filename[:-4])+'.csv'))
            logging.info('name csv when read again')
            logging.info(name_csv)
            df_name_csv = pd.read_csv(name_csv) 

            #==============================================================
            # EXPORT DATA AGAIN 
            #==============================================================
            
            logging.info('export data')

            # Variables
            area = df_name_csv.at[3,'Value']
            logging.info(area)
            polygon = df_name_csv.at[6,'Value']
            stp = df_name_csv.at[7, 'Value'] # spontaneous true positives
            logging.info('stp is :'+str(stp))
            sfn = len(false_negatives) # spontaneous false negatives
            logging.info('sfn is :'+str(sfn))
            sfp = len(false_positives) # spontaneous false positives
            logging.info('sfp is :'+str(sfp))
            ns = str(int(stp) + int(sfn) - int(sfp))
            itp = 'n/a' # induced true positives
            ifn = 'n/a' # induced false negatives
            ifp = 'n/a' # induced false positives 
            ni = 'n/a'
            rhosroi = 'n/a' 
            dnnap = "yolov3_apatite_Nikon_Gent_3000it_50img_December2020.weights" # deep neural network apatite. Currently only one!
            dnnmica = 'n/a' # deep neural network mica 

            # Make new variables to export to the database with the goal on spotting 
            apprecision = float(stp)/(float(stp)+float(sfp))
            apprecision = round(apprecision,2)

            aprecall = float(stp)/(float(stp)+float(sfn))
            aprecall = round(aprecall,2)

            #Executing SQL Statements 
            app = Flask(__name__)

            import storage
            conn = storage.connect()

            # Create app
            mysql = MySQL(app)

            # Connect to database again 
            cur = conn.cursor()
            sql = "INSERT INTO img (name,apprecision, aprecall, labelimg_fn,labelimg_fp) VALUES (%s,%s,%s,%s,%s)" 
            val = (str(filename), str(apprecision),str(aprecall), str(labelimg_fn), str(labelimg_fp)) 
            cur.execute(sql,val)
            
            # Saving the actions performed on the database
            conn.commit()            

            # Close the cursor
            cur.close()
            
            # Export data as .csv file when finished
            from datetime import datetime
            import pandas as pd

            # Make dictionary with names and values
            d = {'Name': ['Method', 'Name apatite', 'Name mica', 'Area', 'Ns', 'Ni', 'Polygon', 'Spont tracks: true positives', 'Spont tracks: false negatives', 'Spont tracks: false positives', 'Induced tracks: true positives' , 'Induced: false negatives', 'Induced: false positives', 'DNN apatite', 'DNN mica', 'apprecision', 'aprecall', 'micaprecision', 'micarecall'], 
                'Value': ['Apatite',filename, 'n/a', area, ns, ni, polygon, stp, sfn, sfp, itp, ifn, ifp, dnnap, dnnmica, apprecision, aprecall, 'n/a', 'n/a'],
                }

            # Print the datafile one more time
            logging.info(d)
            # Export to a panda dataframe
            df = pd.DataFrame(data=d)
            
            # Get name of the csv file 
            name_csv = os.path.join(uploadspath,str(str(filename[:-4])+'.csv'))
            logging.info('send from directory')
            logging.info(name_csv)

            # Make csv file from panda
            df.to_csv(name_csv)
            
            # Send csv to the upload folder
            return send_file(name_csv, as_attachment=True, attachment_filename ='test.jpg', mimetype='image/jpeg') 
        
        # If we're only analysing fission tracks in mica, I called it 'glass'
        elif mineral == 'glass':
            logging.info('glass method detected')     

            loc = os.path.join(uploadspath,filename)
            croppedimage = cv2.imread(loc) 
            logging.info('image read')

            # Make list to store the rectangles for LabelImgFormatter function
            rect_txt_list_mica_fn = list()
            rect_txt_list_mica_fp = list()

            # Get false negatives list
            false_negatives=data['coords_fn'] 
            logging.info('false negatives')
            logging.info(false_negatives)
            logging.info(false_negatives[0])
            logging.info(len(false_negatives))

            # Get false positives list
            false_positives=data['coords_fp']
            logging.info('false positives')
            logging.info(false_positives)
            
            # False negatives: draw rectangles on image
            for i in range(len(false_negatives)):
                l = false_negatives[i]

                x = l['x']
                y = l['y']
                w = l['w']
                h = l['h']
                
                a = int(round(x))
                b = int(round(y ))
                c = int(round(x + w))
                d = int(round(y + h))

                cv2.rectangle(croppedimage, (a,b), (c,d), (0,200,0), 1)

                # Txt file needs fractions
                rect_txt = list()

                x_txt = str((0.5*w + x)/(width))
                rect_txt.append(x_txt[:8])
                y_txt = str((0.5*w + y)/width)
                rect_txt.append(y_txt[:8])
                w_txt = str(w/width)
                rect_txt.append(w_txt[:8])
                h_txt = str(h/width)
                rect_txt.append((h_txt[:8]))
                
                # Append the self-identified rectangle to the list 
                rect_txt_list_mica_fn.append(rect_txt)

            labelimg_fn = labelImgformatter(rect_txt_list_mica_fn)

            # False positives: draw rectangles on image
            for i in range(len(false_positives)):
                l = false_positives[i]

                x = l['x']
                y = l['y']
                w = l['w']
                h = l['h']
                
                a = int(round(x))
                b = int(round(y))
                c = int(round(x + w))
                d = int(round(y + h))

                cv2.rectangle(croppedimage, (a,b), (c,d), (0,0,200), 1)

                # Txt file needs fractions
                rect_txt = list()

                x_txt = str((0.5*w + x)/(width))
                rect_txt.append(x_txt[:8])
                y_txt = str((0.5*w + y)/width)
                rect_txt.append(y_txt[:8])
                w_txt = str(w/width)
                rect_txt.append(w_txt[:8])
                h_txt = str(h/width)
                rect_txt.append((h_txt[:8]))

                # Append the self-identified rectangle to the list 
                rect_txt_list_mica_fp.append(rect_txt)

            labelimg_fp = labelImgformatter(rect_txt_list_mica_fp)

            cv2.imwrite(loc,croppedimage)

            #==============================================================
            # IMPORT DATA FROM CSV FILE
            #==============================================================
            
            import pandas as pd
            # Read csv file 
            name_csv = os.path.join(uploadspath,str(str(filename[:-4])+'.csv'))
            logging.info('name csv when read again')
            logging.info(name_csv)
            df_name_csv = pd.read_csv(name_csv) 

            #==============================================================
            # EXPORT DATA AGAIN 
            #==============================================================
            
            logging.info('export data')

            # Variables
            area = df_name_csv.at[3,'Value']
            logging.info(area)
            polygon = df_name_csv.at[6,'Value']
            stp = 'n/a' # spontaneous true positives
            sfn = 'n/a' # spontaneous false negatives
            sfp = 'n/a' # spontaneous false positives
            ns = 'n/a'
            
            itp = df_name_csv.at[10, 'Value'] # induced true positives 
            logging.info('itp is :'+str(itp))
            ifn = len(false_negatives) # induced false negatives, minus one because the click on "ok ready send data" is also counted as one click (outside the canvas...)
            logging.info('ifn is :'+str(ifn))
            ifp = len(false_positives) # induced false positives 
            ni = str(int(itp) + int(ifn) - int(ifp))
            rhosroi = 'n/a' 
            dnnap = "n/a" # deep neural network apatite
            dnnmica = "yolov3_mica_Nikon_Gent_2000it_50img_December2020.weights" # deep neural network mica. Currently only one!

            # Make new variables to export to the database with the goal on spotting 
            micaprecision = float(itp)/(float(itp)+float(ifp))
            micaprecision = round(micaprecision,2)

            micarecall = float(itp)/(float(itp)+float(ifn))
            micarecall = round(micarecall,2)

            # Executing SQL Statements 
            app = Flask(__name__)

            # Import storage.py file
            import storage
            conn = storage.connect()

            # Create app
            mysql = MySQL(app)

            # Connect to database again 
            cur = conn.cursor()
            sql = "INSERT INTO img (name,micaprecision, micarecall, labelimg_fn,labelimg_fp) VALUES (%s,%s,%s,%s,%s)" 
            val = (str(filename), str(micaprecision),str(micarecall), str(labelimg_fn), str(labelimg_fp)) 
            cur.execute(sql,val)
            
            # Saving the actions performed on the database
            conn.commit()            

            # Close the cursor
            cur.close()
            
            # Export data as .csv file when finished
            from datetime import datetime
            import pandas as pd

            # Make dictionary with names and values
            d = {'Name': ['Method', 'Name apatite', 'Name mica', 'Area', 'Ns', 'Ni', 'Polygon', 'Spont tracks: true positives', 'Spont tracks: false negatives', 'Spont tracks: false positives', 'Induced tracks: true positives' , 'Induced: false negatives', 'Induced: false positives', 'DNN apatite', 'DNN mica', 'apprecision', 'aprecall', 'micaprecision', 'micarecall'], 
                'Value': ['Apatite','n/a', filename, area, ns, ni, polygon, stp, sfn, sfp, itp, ifn, ifp, dnnap, dnnmica, 'n/a', 'n/a', micaprecision,micarecall],
                }

            # Print the datafile one more time
            logging.info(d)

            # Export to a panda dataframe
            df = pd.DataFrame(data=d)
            
            # Get name of the csv file 
            name_csv = os.path.join(uploadspath, str(str(filename[:-4])+'.csv'))
            logging.info('send from directory')
            logging.info(name_csv)
            logging.info(uploadspath)

            # Make csv file from panda
            df.to_csv(name_csv)
            
            # Send csv to the upload folder
            return send_file(name_csv, as_attachment=True, attachment_filename ='test.jpg', mimetype='image/jpeg')
        
        elif mineral == 'annotate':

            # copy glass starts
            logging.info('glass method detected')     

            loc = os.path.join(uploadspath,filename)
            croppedimage = cv2.imread(loc) 
            logging.info('image read')
            logging.info('loc is')
            logging.info(loc)

            # Make list to store the rectangles for LabelImgFormatter function
            rect_txt_list_mica_fn = list()
            rect_txt_list_mica_fp = list()

            # Get false negatives list
            false_negatives=data['coords_fn'] 
            logging.info('false negatives')
            logging.info(false_negatives)
            logging.info(len(false_negatives))

            # Get false positives list
            false_positives=data['coords_fp']
            logging.info('false positives')
            logging.info(false_positives)
            
            # False negatives: draw rectangles on image
            for i in range(len(false_negatives)):
                l = false_negatives[i]

                x = l['x']
                y = l['y']
                w = l['w']
                h = l['h']
                
                a = int(round(x))
                b = int(round(y ))
                c = int(round(x + w))
                d = int(round(y + h))

                # cv2.rectangle(croppedimage, (a,b), (c,d), (0,200,0), 1)

                # Txt file needs fractions
                rect_txt = list()

                x_txt = str((0.5*w + x)/(width))
                rect_txt.append(x_txt[:8])
                y_txt = str((0.5*w + y)/width)
                rect_txt.append(y_txt[:8])
                w_txt = str(w/width)
                rect_txt.append(w_txt[:8])
                h_txt = str(h/width)
                rect_txt.append((h_txt[:8]))
                
                # Append the self-identified rectangle to the list 
                rect_txt_list_mica_fn.append(rect_txt)

            labelimg_fn = labelImgformatter(rect_txt_list_mica_fn)

            # False positives: draw rectangles on image
            for i in range(len(false_positives)):
                l = false_positives[i]

                x = l['x']
                y = l['y']
                w = l['w']
                h = l['h']
                
                a = int(round(x))
                b = int(round(y))
                c = int(round(x + w))
                d = int(round(y + h))

                # cv2.rectangle(croppedimage, (a,b), (c,d), (0,0,200), 1) # skip the rectangle drawing 

                # Txt file needs fractions
                rect_txt = list()

                x_txt = str((0.5*w + x)/(width))
                rect_txt.append(x_txt[:8])
                y_txt = str((0.5*w + y)/width)
                rect_txt.append(y_txt[:8])
                w_txt = str(w/width)
                rect_txt.append(w_txt[:8])
                h_txt = str(h/width)
                rect_txt.append((h_txt[:8]))

                # Append the self-identified rectangle to the list 
                rect_txt_list_mica_fp.append(rect_txt)

            labelimg_fp = labelImgformatter(rect_txt_list_mica_fp)

            cv2.imwrite(loc,croppedimage)

            #==============================================================
            # IMPORT DATA FROM CSV FILE
            #==============================================================
            
            import pandas as pd
            # Read csv file 
            logging.info(filename)
            name_csv = os.path.join(uploadspath,str(str(filename[:-4])+'.csv'))
            logging.info('name csv when read again')
            logging.info(name_csv)
            df_name_csv = pd.read_csv(name_csv) 

            #==============================================================
            # EXPORT DATA AGAIN 
            #==============================================================

            import storage #refers to file storage.py
            conn = storage.connect()

            sql = "INSERT INTO img (name, method, labelimg_fn) VALUES (%s,%s,%s)" 
            val = (str(filename), str(mineral), str(labelimg_fn))
            cur = conn.cursor()
            cur.execute(sql,val)
            
            # Saving the actions performed on the database
            conn.commit()            

            # Close the cursor
            cur.close()
            
            # Export data as .csv file when finished
            from datetime import datetime
            import pandas as pd

            # Make dictionary with names and values
            ifn = labelimg_fn
            logging.info('ifn comes below')
            logging.info(ifn)
            d = {'Name': ['Sample'], 
                'Value': [ifn],
                }

            logging.info('d is ')
            logging.info(d)

            df = pd.DataFrame(data=d)
            
            # Get name of the txt file 
            name_txt = os.path.join(uploadspath, str(str(filename[:-4])+'.txt'))
            logging.info('send from directory')
            logging.info(name_txt)
            logging.info(uploadspath)

            # Make csv file from panda
            df.to_csv(name_txt, columns = ['Value'], header=False, index=False)

            # Send csv to the upload folder
            return send_file(name_txt, as_attachment=True, attachment_filename ='test.txt', mimetype='txt')

# Debugging starts here
if __name__ == "__main__":
    app.run(debug=True)

# # Send an email when an error occurs
# if not app.debug:
#     app.logger.addHandler(mail_handler)