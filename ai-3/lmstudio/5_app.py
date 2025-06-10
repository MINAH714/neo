import lmstudio as lms

image_path = r'C:\Users\kibwa22\Documents\GitHub\neo\ai-3\lmstudio\Lune.png'
image_handle = lms.prepare_image(image_path)

model = lms.llm('google/gemma-3-4b')
chat = lms.Chat()

chat.add_user_message("Describe this image please.", images=[image_handle])

prediction = model.respond(chat)

print(prediction)