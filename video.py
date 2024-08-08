import argparse
import csv

from psychopy import visual, core, event
import serial


liste_video=["Paradigme_video/Stimuli/body1.mp4", "Paradigme_video/Stimuli/body2.mp4", "Paradigme_video/Stimuli/body3.mp4", "Paradigme_video/Stimuli/body5.mp4"]

def play_video_psychopy(chemin, duration, between_stimuli, zoom):
    apparition_stimuli =[]
    longueur_stimuli=[]
    stimuli_liste=[]
    videos=chemin
    win = visual.Window(
        fullscr=True,
        color=[-0.0196, 0.0039, -0.0196],
        units="pix"
    )
    cross_stim = visual.ShapeStim(
        win=win,
        vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
        lineWidth=3,
        closeShape=False,
        lineColor="white"
    )
    #wait_for_trigger()
    global_timer=core.Clock()
    for x in range (len(videos)):
        timer=core.Clock()
        video_path = videos[x]
        movie_stim = visual.MovieStim(
            win=win,
            filename=video_path,
            size=win.size,
            pos=(0, 0),
            flipVert=False,
            flipHoriz=False,
            loop=True,
            units='norm'
        )
        cross_stim.draw()
        win.flip()
        timer.reset()
        apparition_stimuli.append(global_timer.getTime())
        while timer.getTime() < between_stimuli:
            pass
        longueur_stimuli.append(timer)
        stimuli_liste.append("Fixation")
        thezoom = 2 if zoom else 1.4
        movie_stim.size = thezoom
        timer.reset()
        apparition_stimuli.append(global_timer.getTime())
        while timer.getTime() < duration:
            movie_stim.draw()
            win.flip()
        longueur_stimuli.append(timer.getTime())
        stimuli_liste.append(video_path)

    win.close()
    core.quit()
    return apparition_stimuli, longueur_stimuli,stimuli_liste


play_video_psychopy(liste_video,2,2,False)
