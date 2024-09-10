css = '''
<style>
.chat-container {
    max-width: 700px;
    margin: auto;
}
.chat-bubble {
    padding: 10px 20px;
    border-radius: 10px;
    margin: 10px 0;
    max-width: 80%;
}
.bot-bubble {
    background-color: #E0FFFF;
    align-self: flex-end;
    color: #000;
    margin-left: auto;
}
.user-bubble {
    background-color: #4B0082;
    align-self: flex-start;
    color: #fff;
}
.chat-box {
    display: flex;
    flex-direction: column;
}

.response {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}

.response.bot {
    background-color: #Ff6347
}

.response .txt {
  color: #000;
  width = 98%;
}
'''

response_template = '''
<div class="response bot">
    <div class="txt"> {{TXT}} </div>
</div>
'''

user_template = '''
<div class="chat-bubble user-bubble">
    <div class="avatar">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHUvOd8Q-VihyupbJCdgjIR2FxnjGtAgMu3g&s" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

bot_template = '''
<div class="chat-bubble bot-bubble">
    <div class="avatar">
        <img src="data:image/jpeg;base64,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" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''