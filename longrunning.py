def transcribe_gcs(gcs_uri , audio_channel_count):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000, #16000 is better
        language_code='en-US' ,
        max_alternatives=1,
        audio_channel_count=audio_channel_count,
        enable_word_time_offsets=False,
        enable_automatic_punctuation=True,
        model='video'
    )

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result()

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    text = ""
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
        text += "\n"
        text += result.alternatives[0].transcript

    f = open('output.txt', 'w')
    f.write(text)
    f.close()


if __name__ == "__main__" :
    import sys
    print(sys.argv)

    #default values
    url = "gs://abceed-app.appspot.com/resources/output.flac"
    audio_channel_count = 2 #モノラルなら1 ステレオなら2 一致しないと400 Invalid audio channel count
    if len(sys.argv) >= 2 :
        url = sys.argv[1]
    if len(sys.argv) >= 3 :
        audio_channel_count = int(sys.argv[2])
    transcribe_gcs(url , audio_channel_count)
