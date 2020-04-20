# Write in Json from decorator

#Write the contents to file:
# with open(PATH_SAVE + 'streamed_write.json', 'w') as outfile:
#     large_generator_handle = CollecterModel("prod").collect_mail("me", message_id)
#     stream_array = StreamArray(large_generator_handle)
#     for chunk in json.JSONEncoder().iterencode(stream_array):
#         print('Writing chunk: ',chunk)
#         outfile.write(chunk)