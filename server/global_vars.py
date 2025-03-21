import pandas as pd
import threading 

data_lock = threading.Lock()

# map timestamp to avg confusion level
confusion_df = pd.DataFrame(columns=['confusion_level'])

# map timestamp to chunk of lecture transcript
lecture_df = pd.DataFrame(columns=['transcript_chunk'])

DATA_TO_SEND = {'confusion': 0, 'confusing_topics': []}
