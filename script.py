from youtube_transcript_api import YouTubeTranscriptApi

video_ids = ['3pp-RUaUhvY', 'LvrhaYhEb4c', 'hzcD1T_-XK4', 'fduEwKC0OKw', 'X-e2FOhL13Y', 'ZLcAtZIkbBw', '3In3LgSiCcM', 'YrUjuH8zqsY', 
              'wi9uSGrRC9o', 'e4zwTPFkrFw', 'J-p955Needw', 'ENRfckcQ-9Y', 'O-9wllzPEF8', 'axgcspwfXPw', 'Pxlq4KoYEkI', 'Onyn-Y3Ku7I',
              'IF0biMM_2VA', 'bNGYW4CSlZg', 'sa3HX5O1qEA', '_0v98iq-mRs', '-9H0A62JaZY', '1kZq5AdkCyY', 'RM28oR1c4xU', '3SYrf9NAJZE',
              'MYqTovzZW8U', '-GEAyCIgmI8', 'mKUXApaJuSE', 'o1x2iYtRzWI', '2Ika8e2Yr5w', 'Cj1Iin-UKzk', 'zYgjx1qFpkc', 'nFD7hgmw9xs',]

languages = ['ko', 'en']

transcript_list  = list(YouTubeTranscriptApi.get_transcripts(video_ids=video_ids, languages=languages))
transcript_list.pop()

with open('script.txt', 'w', encoding='utf-8') as f:
    for transcript_id in transcript_list:
        for id in video_ids:
            for transcript in transcript_id[id]:
                text = transcript['text']

                if text[0] == '[' or text[0] == '-':
                    continue

                f.write(text)
                f.write('\n')

# []: 자막
# -: 대화

print('Complete!')

