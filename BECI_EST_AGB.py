import os, shutil
#import arcpy
from subprocess import Popen

#current directory where script is placed
cd = os.getcwd()
#pathway varibles that need  be updated per site
lasfiles = '\\las\\' #name of folder in current dir where .las/.laz files are
##plot_path = r'E:\beci_test_LC_jd\Buffers\Battles_LastChance_point_buffers_NAD27.shp' #full path to buffered plot shape file 
##plot_rows = arcpy.SearchCursor(plot_path)
cdlas = cd + lasfiles

#set up environment and create folders
file_path = [cdlas + "gp_bem_tiles\placeholder.txt",
             cdlas + "Canopy\placeholder.txt",
             cd + "\\lasplots\NormalizedPlots\placeholder.txt",
             cd + "\\lasplots\Ground\placeholder.txt",
             cd + "\\lasplots\BareEarth\placeholder.txt",
             cd + "\\lasplots\CloudMetrics\placeholder.txt",
             cd + "\\lasplots\CanopyMaxima\placeholder.txt",
             cd + "\\lasplots\Canopy\placeholder.txt",
             cd + "\\Batch\placeholder.txt"]

def ensure_dir(file_path):
    for path in file_path:
        
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

ensure_dir(file_path)
#move batch files
def movebats(src, trgt):
    filelist=glob.glob(src)
    print(filelist)
    for bat in filelist:
        shutil.move(bat, trgt)
#function to run batchfiles
def runBat(*argv):
    for bat in argv:    
        a = os.getcwd()
        p = Popen( "%s"%(bat), cwd=a)
        p.communicate()



#set up emptylist for plots
##plot_list = []
###add plot IDs to plot list
##for i in plot_rows:
##    value = i.getValue('plot_id')
##    plot_list.append(value)

# file name vars
gp_name = cdlas + 'gp_bem_tiles\groundpoints_'
bem_name = cdlas + 'gp_bem_tiles\SurfaceModel_'
chm_name = cdlas + 'Canopy\chm.dtm'

#fusion path for bat files
gp_txt = 'C:\\fusion\groundfilter /gparam:-1 /wparam:2 /tolerance:0.1 /iterations:10 '
bem_txt = 'C:\\fusion\gridsurfacecreate '
chm_txt = 'C:\\fusion\canopymodel /outlier:2,90 '

#parameters for each model
cellsize = ' 2 '
gen_param = cellsize + 'M M 1 10 1 0 '
ground = '/ground:' 


sa = cd + lasfiles
studyarealas = [ f for f in os.listdir(sa) if os.path.isfile(os.path.join(sa, f)) ]

with open('bare_earth_model.bat', 'w') as out_bem:
    for tile in studyarealas:
        out_bem.write(bem_txt + '/spike:5 ' + bem_name + tile + '.dtm' + gen_param + gp_name + tile + ' \n')
with open('groundpoint.bat', 'w') as out_gp:
    for tile in studyarealas:
        out_gp.write(gp_txt + gp_name + tile + cellsize + cdlas + tile + ' \n')

#run created bat files
runBat('groundpoint.bat','bare_earth_model.bat')

canmax_txt = 'c:\\fusion\canopymaxima /threshold:2 /shape /img24 /summary /projection:'

#CHM
#write new chm .bat
with open('chm.bat', 'w') as out_chm:
    for tile in studyarealas:
        out_chm.write(chm_txt + ground + bem_name + tile + '.dtm ' + chm_name + tile + '.dtm' + gen_param + cdlas + tile + '\n')
with open('canopymax.bat', 'w') as out_canmax:
    for tile in studyarealas:
        out_canmax.write(canmax_txt + chm_name + tile + '.dtm ' + chm_name + tile + '.dtm ' + cm_name + tile + '.csv' + '\n')

#run chm bat
runBat('chm.bat','canopymax.bat')



### write a btach file to clip each plot from the study area using lastools
##wdplots = cd + "\\lasplots"
##lasclip_txt = "c:\lastools\\bin\lasclip"
##las_in = ' -i ' + cdlas + '*.las'   ## wrks w sigle or tiles
##poly = ' -poly ' + plot_path + ' -split'
##plots_out = ' -o ' + wdplots + '\\plot.las'
##
###add var to bat file
##out_clip = open('clipplots.bat', 'w')
##out_clip.write(lasclip_txt + las_in + ' -merged' + poly + plots_out ) #merge switch used when input files are tiled
##out_clip.close()
##
###run the bat
##runBat('clipplots.bat')
##
##
##
###now to run all that ish again on the plot lvl
###list the plots inn the sub folder
##
##plots = [ f for f in os.listdir(wdplots) if os.path.isfile(os.path.join(wdplots, f)) ]
##
### file name vars
##gp_name = wdplots + '\\Ground\groundpoints_'
##bem_name = wdplots + '\\BareEarth\SurfaceModel_'
##chm_name = wdplots + '\\Canopy\chm_'
##canmax_name = wdplots + '\\CanopyMaxima\canopymaxima_'
##wdCanMax = wdplots + '\\CanopyMaxima'
##
### set up for canopy maxima
##canmax_txt = "c:\\fusion\canopymaxima /threshold:2 /summary "
##
##
###write new bat file
##with open('plots_gp.bat', 'w') as out_plots_gp:
##    for plot, pl in zip(plots, plot_list):
##        out_plots_gp.write(gp_txt + gp_name + pl + plot + cellsize + wdplots + '\\' + plot + '\n')
##with open('plots_bem.bat', 'w') as out_plots_bem:
##    for plot, pl in zip(plots, plot_list):
##        out_plots_bem.write(bem_txt + '/spike:5 ' + bem_name + pl + plot + '.dtm' + gen_param + gp_name + pl + plot + '\n')
##with open('plots_chm.bat', 'w') as out_plots_chm:
##    for plot, pl in zip(plots, plot_list):
##        out_plots_chm.write(chm_txt + '/ground:' + bem_name + pl + plot + '.dtm ' + chm_name + pl + plot + '.dtm' + gen_param + wdplots + '\\' + plot + '\n')
##with open('plots_canmax.bat', 'w') as out_plots_canmax:
##    for plot, pl in zip(plots, plot_list):
##        out_plots_canmax.write(canmax_txt + chm_name + pl + plot + '.dtm ' + canmax_name + pl + plot + '.csv' + '\n' ) #no need for canmax ground switch bc chm's are already normalized
##        
##
###run the batzzz
##runBat('plots_gp.bat','plots_bem.bat','plots_chm.bat','plots_canmax.bat')
##
###copy canmax concatenate .py to correct dir
##shutil.copy2( cd + '\\mergecsv.py', wdCanMax) # target filename is /dst/dir/file.ext
##
###run can max summary files
##runBat('python mergecsv.py') 
##
###delete copy of merge
##os.remove(wdCanMax + '\\mergecsv.py')
##
##cm_text = "c:\\fusion\cloudmetrics /id /minht:2 /above:2 "
##norm_text = "c:\lastools\\bin\lasheight -i "
##norm_op = " -o " + wdplots + "\\NormalizedPlots\\norm_"
##
##with open('plots_norm.bat', 'w') as out_plots_norm:
##    for plot, pl in zip(plots, plot_list):
##        out_plots_norm.write(norm_text + wdplots + "\\" + plot + " -replace_z -ground_points " + gp_name + pl + plot + norm_op + pl + plot + " \n")
##
##with open('plots_cm.bat', 'w') as out_plots_cm:
##    out_plots_cm.write(cm_text + wdplots + "\\NormalizedPlots\*.las " + wdplots + "\\CloudMetrics\CloudMetrics.csv" + " \n")
##
##p = Popen('plots_norm.bat', cwd=cd)
##p.communicate()
##p = Popen('plots_cm.bat', cwd=cd)
##p.communicate()
##
###clean up all the batch files laying around
##movebats(cd + "\\*.bat", cd + "\\Batch")
##






