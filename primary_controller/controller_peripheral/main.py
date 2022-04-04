import time
import driver.utils as utils

from functionality.board import Board
from functionality.menu import Menu
from functionality.communication import Communication as Com

# controls if start screen should be shown
show_start_screen = True

def main():
  """ Main function, contains event loop """
  # led flash
  Board.status_led.show_bootup()
  # auxiliary initializations
  Board.auxiliary_init()
  # buzzer and vmotor indicating running
  Board.buzzer.sound_bootup()
  Board.vmotor.slight_vibration()

  # waiting for main controller to connect
  while True:
    msg = Board.uart1_com.read_all(Com.START)
    if msg != None:
      Board.uart1_com.send(Com.START, Com.BOOT_UP)
      break

  # wait for start screen to finish if not already
  while not utils.start_screen_exited():
    time.sleep_ms(200)

  # undisplay initialization screen
  if show_start_screen:
    Board.main_display.notify_to_quit()

  # begin operation
  Board.begin_operation()
  time.sleep_ms(100)

  # Example useage of Board.uart1 and Board.button
  #
  # while True:
  #   # UART
  #   if Board.is_uart1_pending():
  #     messages = Board.get_all_uart1_message()
  #     print(f"UART: {messages}")
  #   # BUTTON
  #   if Board.is_button_pending():
  #     messages = Board.get_all_button_message()
  #     print(f"BUTTON: {messages}")
  #   time.sleep_ms(10)

  # set current display to main menu
  current_menu = Menu.main_menu

  # menu loop
  while True:
    if current_menu == Menu.main_menu:
      choice_idx = Board.display_menu_and_get_choice(current_menu, Board.main_display, 0)

      if choice_idx == 0: # Start Operation
        current_menu = Menu.main_menu
      elif choice_idx == 1: # Settings
        current_menu = Menu.settings_menu
      elif choice_idx == 2: # Snake
        Board.begin_snake_game(Board.main_display, max_score=20)
        current_menu = Menu.main_menu

    elif current_menu == Menu.settings_menu:
      choice_idx = Board.display_menu_and_get_choice(current_menu, Board.main_display, -1)

      if choice_idx == 0: # Load Config
        current_menu = Menu.settings_menu
      elif choice_idx == 1: # Create Config
        user_string = Board.display_keyboard_and_get_input(Board.main_display, "File Name", 2)
        
        if user_string == None: # Cancel
          current_menu = Menu.settings_menu
        else: # Confirm
          print(user_string)
          current_menu = Menu.settings_menu

      elif choice_idx == 2: # View Config
        with open("main.py", "r") as f:
          # normal file contains "\r\n" as new line character
          Board.begin_text_viewer(Board.main_display, f.read(), True, "\r\n") 
        current_menu = Menu.settings_menu
      elif choice_idx == 3: # Back
        current_menu.change_highlight(0) # reset highlight
        current_menu = Menu.main_menu

if __name__ == '__main__':
  # !!! Do NOT modify this function !!!
  # allow REPL to run in parallel with main function
  utils.execute_main(main, start_screen=show_start_screen)
