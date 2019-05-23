"""
Script to calculate number of words per minute for each GoT episode.
script to read srt files is taken from github: ndunn219/srt_to_txt.py
script to make a pretty plot is from: http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
"""
import re
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

def is_time_stamp(l):
  if l[:2].isnumeric() and l[2] == ':':
    return True
  return False

def has_letters(line):
  if re.search('[a-zA-Z]', line):
    return True
  return False

def has_no_text(line):
  l = line.strip()
  if not len(l):
    return True
  if l.isnumeric():
    return True
  if is_time_stamp(l):
    return True
  if l[0] == '(' and l[-1] == ')':
    return True
  if not has_letters(line):
    return True
  return False

def is_lowercase_letter_or_comma(letter):
  if letter.isalpha() and letter.lower() == letter:
    return True
  if letter == ',':
    return True
  return False

def clean_up(readfile):
    """
    Get rid of all non-text lines and
    try to combine text broken into multiple lines
    """
    new_lines = []
    word_list = []
    for line in lines[1:]:
        if has_no_text(line):
            continue
        elif len(new_lines) and is_lowercase_letter_or_comma(line[0]):
        #combine with previous line
            new_lines[-1] = new_lines[-1].strip() + ' ' + line
        else:
      #append line
             words = line.split()
             for word in words:
                 if word[0].isalpha():
                     word_list.append(word)
    # for each word in the line:
    
             new_lines.append(line)
    return new_lines, word_list


if __name__ == '__main__':
    wordcount = []
    files = glob.glob(os.path.join(os.getcwd(),'gotsubtitles\*'))
    seasons =   {'1':[0,10],
                 '2':[10,20],
                 '3':[20,30],
                 '4':[30,40],
                 '5':[40,49],
                 '6':[49,59],
                 '7':[59,66],
                 '8':[66,72]
                 }     
            
    for file in files:
        if file[-4:] != '.zip'       :
            for file_name in glob.glob(file+'\*.srt'):
                if file_name[-4:]=='.srt':
                    file_encoding = 'utf-8'
                    with open(file_name, encoding='utf-8', errors='replace') as f:
                        lines = f.readlines()
                        last_lines = lines[-10:]
                        for l in last_lines:
                            if is_time_stamp(l):
                                hour = float(l[1:2])
                                minute = float(l[3:5])
                                length = minute+hour*60
                        
                        new_lines, word_list = clean_up(lines)
                        wordcount.append(len(word_list)/length)
                        new_file_name = file_name[:-4] + '.txt'
    x = list(range(len(wordcount)))
    z = np.polyfit(x, wordcount, 1)
    p = np.poly1d(z)
    
    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)    
  
    #START PLOTTING
    plt.figure(figsize=(12, 8))    
      
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
      
    # Ensure that the axis ticks only show up on the bottom and left of the plot.    
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()    
      
    # Limit the range of the plot to only where the data is.    
    # Avoid unnecessary whitespace.    
    plt.ylim(10, 70)    
    plt.xlim(0, 72)    
      
    # Make sure your axis ticks are large enough to be easily read.    
    # You don't want your viewers squinting to read your plot.    
    plt.yticks(range(10, 71, 10), [str(x) for x in range(10, 71, 10)], fontsize=14)    
    plt.xticks(fontsize=14)    
    for y in range(20, 71, 10):    
        plt.plot(range(0, 72), [y] * len(range(0, 72)), "--", lw=0.5, color="black", alpha=0.3)    
  
    
    plt.plot(x,p(x),"--", lw=4, color="black", alpha=0.5)
    
    for j in seasons:
        i = seasons[j]
        plt.plot(x[i[0]:i[1]],wordcount[i[0]:i[1]], color=tableau20[int(j)])
        plt.text(73, 78-int(j)*8, 'Season {}'.format(j), fontsize=14, color=tableau20[int(j)])  
        
    plt.text(35, 75, "Number of words per minute for each episode (Game of Thrones Season 1-8)"    
       , fontsize=17, ha="center")    

    plt.text(0, -1, "Data source: https://opensubtitles.org "    
       "\nAuthor: mrquart github:mrquart"    
       "\nNote: code and list of subtitles are available on www.github.com", fontsize=10)  
    plt.savefig("got-words-eopisode.png", bbox_inches="tight")  

"""
NOTES
- The following srt files were used:
- Season 1-5 is from the same author: game.of.thrones.s01.e01.winter.is.coming.(2011).eng.1cd.(7066325)
GoT S01E01 Winter Is Coming 720p.English.srt
GoT S01E02 The Kingsroad 720p.English.srt
GoT S01E03 Lord Snow 720p.English.srt
GoT S01E04 Cripples, Bastards, and Broken Things 720p.English.srt
GoT S01E05 The Wolf and the Lion 720p.English.srt
GoT S01E06 A Golden Crown 720p.English.srt
GoT S01E07 You Win or You Die 720p.English.srt
GoT S01E08 The Pointy End 720p.English.srt
GoT S01E09 Baelor 720p.English.srt
GoT S01E10 Fire and Blood 720p.English.srt
GoT S02E01 The North Remembers 720p.English.srt
GoT S02E02 The Night Lands 720p.English.srt
GoT S02E03 What Is Dead May Never Die 720p.English.srt
GoT S02E04 Garden of Bones 720p.English.srt
GoT S02E05 The Ghost Of Harrenhal 720p.English.srt
GoT S02E06 The Old Gods And The New 720p.English.srt
GoT S02E07 A Man Without Honor 720p.English.srt
GoT S02E08 The Prince of Winterfell 720p.English.srt
GoT S02E09 Blackwater 720p.English.srt
GoT S02E10 Valar Morghulis 720p.English.srt
GoT S03E01 Valar Dohaeris 720p.English.srt
GoT S03E02 Dark Wings, Dark Words 720p.English.srt
GoT S03E03 Walk of Punishment 720p.English.srt
GoT S03E04 And Now His Watch Is Ended 720p.English.srt
GoT S03E05 Kissed by Fire 720p.English.srt
GoT S03E06 The Climb 720p.English.srt
GoT S03E07 The Bear and the Maiden Fair 720p.English.srt
GoT S03E08 Second Sons 720p.English.srt
GoT S03E09 The Rains of Castamere 720p.English.srt
GoT S03E10 Mhysa 720p.English.srt
GoT S04E01 Two Swords 720p.English.srt
GoT S04E02 The Lion and The Rose 720p.English.srt
GoT S04E03 Breaker of Chains 720p.English.srt
GoT S04E04 Oathkeeper 720p.English.srt
GoT S04E05 First of His Name 720p.English.srt
GoT S04E06 The Laws of Gods and Men 720p.English.srt
GoT S04E07 Mockingbird 720p.English.srt
GoT S04E08 The Mountain and the Viper 720p.English.srt
GoT S04E09 The Watchers on the Wall 720p.English.srt
GoT S04E10 The Children 720p.English.srt
GoT.S05E01.The.Wars.To.Come.720p.English.srt
GoT.S05E02.The.House.Of.Black.And.White.720p.English.srt
GoT.S05E03.High.Sparrow.720p.English.srt
GoT.S05E04.Sons.Of.The.Harpy.720p.English.srt
GoT.S05E05.Kill.The.Boy.720p.English.srt
GoT.S05E06.Unbowed.Unbent.Unbroken.720p.English.srt
GoT.S05E07.The.Gift.720p.English.srt
GoT.S05E08.Hardhome.720p.English.srt
GoT.S05E09.The.Dance.Of.Dragons.720p.English.srt
Game_of_Thrones_S06E01_x265_1080p_BluRay_30nama_30NAMA.srt
Game.of.Thrones.S06E02.PROPER.HDTV.x264-BATV.srt
Game.of.Thrones.S06E03.HDTV.x264-KILLERS.srt
Game.of.Thrones.S06E04.720p.HDTV.x264-AVS.srt
Game.of.Thrones.S06E05.HDTV.x264-KILLERS.srt
Game.of.Thrones.S06E06.720p.HDTV.x264-AVS.srt
Game.of.Thrones.S06E07.HDTV.x264-KILLERS.srt
Game.of.Thrones.S06E08.HDTV.x264-KILLERS.srt
Game.of.Thrones.S06E09.HDTV.x264-KILLERS.srt
Game.of.Thrones.S06E10.720p.HDTV.x265.FLEET-KILLER eng.srt
game.of.thrones.s07e01.720p.web.h264-tbs.srt
Game.of.Thrones.S07E02.Stormborn.AMZN.WEBRip.DDP2.0.x264-GoT.srt
Game.of.Thrones.S07E03.The.Queens.Justice.720p.AMZN.WEBRip.D.srt
Game.of.Thrones.S07E04.HDTV.x264-SVA.srt
Game.of.Thrones.S07E05.720p.WEB.h264-TBS.srt
Game.of.Thrones.S07E06.1080p.HDTV.Good Audio.Leaked. - .ECLiPSE.srt
Game.of.Thrones.S07E07.The.Dragon.and.the.Wolf.720p.AMZN.WEB-DL.DDP5.1.H.264-GoT.srt
Game.of.Thrones.S08E01.Kings.Landing.720p.AMZN.WEB-DL.DDP5.1.H.264-GoT.srt
game.of.thrones.s08e02.web.h264-memento.srt
Game.of.Thrones.S08E03.WEB.H264-MEMENTO-HI.srt
Game.of.Thrones.S08E04.720p.AMZN.WEBRip.DDP5.1.x264-GoT.srt
game.of.thrones.s08e05.web.h264-memento.srt
Game.of.Thrones.S08E06.WEB.H264-MEMENTO.srt 
"""

