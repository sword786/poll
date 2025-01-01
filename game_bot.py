import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters  # Updated import

# Start the bot and show instructions
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome to the Guess the Number Game! I have chosen a number between 1 and 100. "
        "Try to guess it by typing your guess. Type /quit to exit."
    )
    # Store the random number in the user's chat data
    context.user_data['number'] = random.randint(1, 100)
    context.user_data['attempts'] = 0

# Handle the user's guess
async def guess(update: Update, context: CallbackContext) -> None:
    if 'number' not in context.user_data:
        await update.message.reply_text("Use /start to begin the game.")
        return

    try:
        user_guess = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return

    target_number = context.user_data['number']
    context.user_data['attempts'] += 1

    if user_guess < target_number:
        await update.message.reply_text("Too low! Try again.")
    elif user_guess > target_number:
        await update.message.reply_text("Too high! Try again.")
    else:
        await update.message.reply_text(
            f"Congratulations! You guessed the number {target_number} in {context.user_data['attempts']} attempts. Type /start to play again."
        )
        del context.user_data['number']  # End the game

# Quit the game
async def quit_game(update: Update, context: CallbackContext) -> None:
    if 'number' in context.user_data:
        del context.user_data['number']
    await update.message.reply_text("Game ended. Type /start to play again.")

# Main function to set up the bot
def main():
    token = "7698747229:AAHlqpck1_NZwAu019Soq0gmI0LabwpbOn4"  # Replace with your bot's token
    application = Application.builder().token(token).build()  # Use Application builder for version 20+

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quit", quit_game))
    
    # Message handler for guesses
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))
    
    # Start polling for updates (this method manages the event loop internally)
    application.run_polling()

if __name__ == '__main__':
    main()
