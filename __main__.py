import os

fileDir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(fileDir, 'DatabaseManagement/time_vortex.db')

if os.path.exists(filename):
    import Interface.start_dialogue

else:
    from WebParse.get_episodes import get_episodes
    get_episodes()
    import Interface.start_dialogue
