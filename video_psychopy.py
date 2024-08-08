import argparse
import csv

from psychopy import visual, core, event
import serial


def wait_for_trigger(port='COM3', baudrate=9600, trigger_char='s'):
    with serial.Serial(port, baudrate=baudrate) as ser:
        trigger = ser.read().decode('utf-8')
        while trigger != trigger_char:
            trigger = ser.read().decode('utf-8')
        print("Trigger received")


def reading(filename):
    with open(filename, "r") as fichier:
        ma_liste = [line.strip() for line in fichier]
    print("okk")
    print(ma_liste)
    return ma_liste


def play_video_psychopy(chemin, duration, between_stimuli, zoom):
    apparition_stimuli = []
    longueur_stimuli = []
    stimuli_liste = []
    videos = reading(chemin)
    for x in range(len(videos)):
        videos[x] = "Paradigme_video/Stimuli/" + videos[x]
    print(videos)
    win = visual.Window(
        fullscr=True,
        #color = [0, 0, 1],
        #color = [1,0,0],
        color= [-0.042607843137254943, 0.0005215686274509665, -0.025607843137254943],
        units="pix"
    )
    cross_stim = visual.ShapeStim(
        win=win,
        vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
        lineWidth=3,
        closeShape=False,
        lineColor="white"
    )
    wait_for_trigger()
    global_timer = core.Clock()
    thezoom = 1.3+(0.77*zoom/100)
    #thezoom = 1.4*zoom/100
    #thezoom = 2 if zoom else 1.4
    for x in range(len(videos)):
        timer = core.Clock()
        video_path = videos[x]
        movie_stim = visual.MovieStim(
            win=win,
            filename=video_path,
            size=[1920,1080],
            pos=(0, 0),
            opacity=1.0,
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
        longueur_stimuli.append(timer.getTime())
        stimuli_liste.append("Fixation")
        movie_stim.size = thezoom
        timer.reset()
        apparition_stimuli.append(global_timer.getTime())
        while timer.getTime() < duration:
            movie_stim.draw()
            win.flip()
        longueur_stimuli.append(timer.getTime())
        stimuli_liste.append(video_path)

    cross_stim.draw()
    win.flip()
    timer.reset()
    apparition_stimuli.append(global_timer.getTime())
    while timer.getTime() < between_stimuli:
        pass
    longueur_stimuli.append(timer.getTime())
    stimuli_liste.append("Fixation")
    win.close()
    return longueur_stimuli, apparition_stimuli, stimuli_liste

def write_tsv(onset, duration, file_stimuli, trial_type, filename="output.tsv"):
    print("ici ????")
    with open(filename, mode='w', newline='') as file:
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow(['onset', 'duration', 'trial_type', 'stim_file'])
        for i in range(len(onset)):
            tsv_writer.writerow([onset[i], duration[i], trial_type[i], file_stimuli[i]])


def main(duration, betweenstimuli, file, zoom, output_file):
    #stimulus_times, stimulus_apparition, stimuli, orientation = static_images_psychopy(file, duration, betweenstimuli, zoom)
    print("okkkffffffkkkkk")

    stimulus_times, stimulus_apparition, stimuli = play_video_psychopy(file, duration, betweenstimuli, zoom)
    liste_trial = []
    liste_lm = []
    count = 0
    print("okkkkkkkk")
    for x in stimuli:
        if x == "Fixation":
            liste_lm.append(count)
            liste_trial.append("Fixation")
        else:
            liste_trial.append("Stimuli")
        count += 1
    print("oooooooooo")
    for x in liste_lm:
        stimuli[x] = "None"
    write_tsv(stimulus_apparition, stimulus_times, stimuli, liste_trial, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=int, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=int, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")


    args = parser.parse_args()

    main(args.duration, args.betweenstimuli, "Paradigme_video/"+args.file, args.zoom, "Fichiers_output/"+args.output_file+".tsv")
    """
    duration = 1
    betweenstimuli = 1
    file = "Paradigme_video/chemin.txt"
    zoom = True
    output_file = "Fichiers_output/videotesddt.tsv"

    main(duration, betweenstimuli, file, zoom, output_file)
    """