# import tkinter as tk
# from tkinter import ttk, scrolledtext, messagebox
# import threading
# import logging
# from datetime import datetime
# from config import Config

# logger = logging.getLogger(__name__)

# class ModernVoiceAssistantGUI:
#     def __init__(self, start_callback, stop_callback, talk_callback=None):
#         self.config = Config()
#         self.start_callback = start_callback
#         self.stop_callback = stop_callback
#         self.talk_callback = talk_callback
#         self.is_listening = False
        
#         self.create_main_window()
#         self.create_widgets()
#         self.setup_styles()
        
#         # Auto-start if configured
#         if self.config.get("auto_start"):
#             self.root.after(1000, self.start_listening)
    
#     def create_main_window(self):
#         """Create the main window with modern styling"""
#         self.root = tk.Tk()
#         self.root.title("Eight - Voice Assistant")
#         self.root.geometry("600x500")
#         self.root.minsize(500, 400)
#         self.root.configure(bg='#2c3e50')
        
#         # Center window on screen
#         self.center_window()
        
#         # Configure window icon and properties
#         try:
#             # You can add an icon file here
#             # self.root.iconbitmap('icon.ico')
#             pass
#         except:
#             pass
    
#     def center_window(self):
#         """Center the window on screen"""
#         self.root.update_idletasks()
#         x = (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2
#         y = (self.root.winfo_screenheight() - self.root.winfo_height()) // 2
#         self.root.geometry(f"+{x}+{y}")
    
#     def setup_styles(self):
#         """Setup modern styling"""
#         style = ttk.Style()
#         style.theme_use('clam')
        
#         # Configure button styles
#         style.configure('Action.TButton',
#                        font=('Segoe UI', 10, 'bold'),
#                        padding=10)
        
#         style.configure('Talk.TButton',
#                        font=('Segoe UI', 9),
#                        padding=5)
#     def start_live_talk(self):
#         """Start live conversation mode"""
#         if self.talk_callback:
#             try:
#                 self.update_text("🎙️ Starting live conversation mode...")
#                 self.live_talk_button.configure(text="🛑 End Live", command=self.end_live_talk)
#                 threading.Thread(
#                     target=lambda: self.talk_callback("start live talk"),
#                     daemon=True
#                 ).start()
#             except Exception as e:
#                 self.update_text(f"❌ Error starting live talk: {str(e)}")
    
#     def end_live_talk(self):
#         """End live conversation mode"""
#         if self.talk_callback:
#             try:
#                 self.update_text("🛑 Ending live conversation mode...")
#                 self.live_talk_button.configure(text="🎙️ Live Talk", command=self.start_live_talk)
#                 threading.Thread(
#                     target=lambda: self.talk_callback("end live talk"),
#                     daemon=True
#                 ).start()
#             except Exception as e:
#                 self.update_text(f"❌ Error ending live talk: {str(e)}")

    
#     def create_widgets(self):
#         """Create all GUI widgets"""
#         # Main title
#         title_frame = tk.Frame(self.root, bg='#2c3e50')
#         title_frame.pack(fill='x', padx=20, pady=10)
        
#         title_label = tk.Label(
#             title_frame,
#             text="🎙️ EIGHT Voice Assistant",
#             font=('Segoe UI', 18, 'bold'),
#             fg='#ecf0f1',
#             bg='#2c3e50'
#         )
#         title_label.pack()
        
#         # Status indicator
#         self.status_frame = tk.Frame(self.root, bg='#2c3e50')
#         self.status_frame.pack(fill='x', padx=20, pady=5)
        
#         self.status_indicator = tk.Label(
#             self.status_frame,
#             text="●",
#             font=('Arial', 20),
#             fg='#e74c3c',  # Red when not listening
#             bg='#2c3e50'
#         )
#         self.status_indicator.pack(side='left')
        
#         self.status_label = tk.Label(
#             self.status_frame,
#             text="Ready to start",
#             font=('Segoe UI', 11),
#             fg='#bdc3c7',
#             bg='#2c3e50'
#         )
#         self.status_label.pack(side='left', padx=10)
        
#         # Control buttons frame
#         controls_frame = tk.Frame(self.root, bg='#2c3e50')
#         controls_frame.pack(fill='x', padx=20, pady=10)
        
#         # Start/Stop button
#         self.main_button = ttk.Button(
#             controls_frame,
#             text="🎤 Start Listening",
#             command=self.toggle_listening,
#             style='Action.TButton'
#         )
#         self.main_button.pack(side='left', padx=5)
        
#         # Talk button
#         self.talk_button = ttk.Button(
#             controls_frame,
#             text="💬 Talk",
#             command=self.start_talking,
#             style='Talk.TButton'
#         )
#         self.talk_button.pack(side='left', padx=5)
#         # Live Talk button (add after the Talk button)
#         self.live_talk_button = ttk.Button(
#             controls_frame,
#             text="🎙️ Live Talk",
#             command=self.start_live_talk,
#             style='Talk.TButton'
#         )
#         self.live_talk_button.pack(side='left', padx=5)

#         # Settings button
#         self.settings_button = ttk.Button(
#             controls_frame,
#             text="⚙️ Settings",
#             command=self.open_settings,
#             style='Talk.TButton'
#         )
#         self.settings_button.pack(side='right', padx=5)
        
#         # Conversation area
#         conversation_frame = tk.LabelFrame(
#             self.root,
#             text="Conversation",
#             font=('Segoe UI', 10, 'bold'),
#             fg='#ecf0f1',
#             bg='#34495e',
#             relief='flat',
#             padx=10,
#             pady=10
#         )
#         conversation_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
#         self.text_area = scrolledtext.ScrolledText(
#             conversation_frame,
#             wrap=tk.WORD,
#             width=60,
#             height=15,
#             font=('Consolas', 10),
#             bg='#2c3e50',
#             fg='#ecf0f1',
#             insertbackground='#ecf0f1',
#             relief='flat',
#             padx=10,
#             pady=10
#         )
#         self.text_area.pack(fill='both', expand=True)
        
#         # Quick actions frame
#         actions_frame = tk.LabelFrame(
#             self.root,
#             text="Quick Actions",
#             font=('Segoe UI', 9),
#             fg='#ecf0f1',
#             bg='#34495e',
#             relief='flat'
#         )
#         actions_frame.pack(fill='x', padx=20, pady=(0, 10))
        
#         # Quick action buttons
#         quick_buttons_frame = tk.Frame(actions_frame, bg='#34495e')
#         quick_buttons_frame.pack(fill='x', padx=5, pady=5)
        
#         quick_actions = [
#             ("📺 YouTube", lambda: self.quick_command("open youtube")),
#             ("🌦️ Weather", lambda: self.quick_command("weather")),
#             ("🕐 Time", lambda: self.quick_command("what time is it")),
#             ("📸 Screenshot", lambda: self.quick_command("take screenshot")),
#         ]
        
#         for i, (text, command) in enumerate(quick_actions):
#             btn = ttk.Button(
#                 quick_buttons_frame,
#                 text=text,
#                 command=command,
#                 style='Talk.TButton'
#             )
#             btn.pack(side='left', padx=2, fill='x', expand=True)
        
#         # Add initial welcome message
#         self.update_text("Welcome to Eight Voice Assistant! 🎉")
#         self.update_text("Click 'Start Listening' or say 'Eight' to activate.")
#         self.update_text("Use the 'Talk' button for conversation mode.")
    
#     def toggle_listening(self):
#         """Toggle listening state"""
#         if not self.is_listening:
#             self.start_listening()
#         else:
#             self.stop_listening()
    
#     def start_listening(self):
#         """Start voice assistant"""
#         try:
#             self.is_listening = True
#             self.main_button.configure(text="🛑 Stop Listening")
#             self.status_indicator.configure(fg='#27ae60')  # Green
#             self.status_label.configure(text="Listening for 'Eight'...")
            
#             # Run in separate thread
#             threading.Thread(target=self.start_callback, daemon=True).start()
            
#             self.update_text("🎤 Voice assistant started. Say 'Eight' to activate!")
            
#         except Exception as e:
#             self.update_text(f"❌ Error starting assistant: {str(e)}")
#             logger.error(f"Start listening error: {e}")
    
#     def stop_listening(self):
#         """Stop voice assistant"""
#         try:
#             self.is_listening = False
#             self.main_button.configure(text="🎤 Start Listening")
#             self.status_indicator.configure(fg='#e74c3c')  # Red
#             self.status_label.configure(text="Stopped")
            
#             self.stop_callback()
#             self.update_text("🛑 Voice assistant stopped.")
            
#         except Exception as e:
#             self.update_text(f"❌ Error stopping assistant: {str(e)}")
#             logger.error(f"Stop listening error: {e}")
    
#     def start_talking(self):
#         """Start conversation mode"""
#         if self.talk_callback:
#             try:
#                 self.update_text("💬 Conversation mode activated...")
#                 threading.Thread(
#                     target=lambda: self.talk_callback("start conversation"),
#                     daemon=True
#                 ).start()
#             except Exception as e:
#                 self.update_text(f"❌ Error starting conversation: {str(e)}")
#         else:
#             self.update_text("💬 Talk mode not available")
    
#     def quick_command(self, command):
#         """Execute quick command"""
#         if self.talk_callback:
#             try:
#                 self.update_text(f"⚡ Quick command: {command}")
#                 threading.Thread(
#                     target=lambda: self.talk_callback(command),
#                     daemon=True
#                 ).start()
#             except Exception as e:
#                 self.update_text(f"❌ Error executing command: {str(e)}")
    
#     def open_settings(self):
#         """Open settings dialog"""
#         SettingsDialog(self.root, self.config)
    
#     def update_text(self, text):
#         """Update text area with timestamp"""
#         timestamp = datetime.now().strftime("%H:%M:%S")
#         formatted_text = f"[{timestamp}] {text}\n"
        
#         # Update in main thread
#         self.root.after(0, self._update_text_safe, formatted_text)
    
#     def _update_text_safe(self, text):
#         """Thread-safe text update"""
#         self.text_area.insert(tk.END, text)
#         self.text_area.see(tk.END)
        
#         # Keep only last 100 lines
#         lines = self.text_area.get("1.0", tk.END).split('\n')
#         if len(lines) > 100:
#             self.text_area.delete("1.0", f"{len(lines)-100}.0")
    
#     def run(self):
#         """Start the GUI main loop"""
#         try:
#             self.root.mainloop()
#         except KeyboardInterrupt:
#             self.stop_listening()

# class SettingsDialog:
#     def __init__(self, parent, config):
#         self.config = config
#         self.dialog = tk.Toplevel(parent)
#         self.dialog.title("Settings")
#         self.dialog.geometry("400x300")
#         self.dialog.resizable(False, False)
#         self.dialog.configure(bg='#2c3e50')
        
#         # Make dialog modal
#         self.dialog.transient(parent)
#         self.dialog.grab_set()
        
#         self.create_settings_widgets()
        
#         # Center dialog
#         self.dialog.update_idletasks()
#         x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
#         y = parent.winfo_y() + (parent.winfo_height() - 300) // 2
#         self.dialog.geometry(f"+{x}+{y}")
    
#     def create_settings_widgets(self):
#         """Create settings widgets"""
#         # Title
#         title = tk.Label(
#             self.dialog,
#             text="⚙️ Assistant Settings",
#             font=('Segoe UI', 14, 'bold'),
#             fg='#ecf0f1',
#             bg='#2c3e50'
#         )
#         title.pack(pady=10)
        
#         # Settings frame
#         settings_frame = tk.Frame(self.dialog, bg='#2c3e50')
#         settings_frame.pack(fill='both', expand=True, padx=20)
        
#         # Speech rate
#         tk.Label(
#             settings_frame,
#             text="Speech Rate:",
#             fg='#ecf0f1',
#             bg='#2c3e50'
#         ).pack(anchor='w', pady=(10, 5))
        
#         self.rate_var = tk.IntVar(value=self.config.get("speech_rate"))
#         rate_scale = tk.Scale(
#             settings_frame,
#             from_=100,
#             to=300,
#             orient='horizontal',
#             variable=self.rate_var,
#             bg='#34495e',
#             fg='#ecf0f1',
#             highlightthickness=0
#         )
#         rate_scale.pack(fill='x', pady=(0, 10))
        
#         # Volume
#         tk.Label(
#             settings_frame,
#             text="Volume:",
#             fg='#ecf0f1',
#             bg='#2c3e50'
#         ).pack(anchor='w', pady=(0, 5))
        
#         self.volume_var = tk.DoubleVar(value=self.config.get("volume"))
#         volume_scale = tk.Scale(
#             settings_frame,
#             from_=0.1,
#             to=1.0,
#             resolution=0.1,
#             orient='horizontal',
#             variable=self.volume_var,
#             bg='#34495e',
#             fg='#ecf0f1',
#             highlightthickness=0
#         )
#         volume_scale.pack(fill='x', pady=(0, 10))
        
#         # Auto-start checkbox
#         self.auto_start_var = tk.BooleanVar(value=self.config.get("auto_start"))
#         auto_start_check = tk.Checkbutton(
#             settings_frame,
#             text="Auto-start assistant",
#             variable=self.auto_start_var,
#             fg='#ecf0f1',
#             bg='#2c3e50',
#             selectcolor='#34495e'
#         )
#         auto_start_check.pack(anchor='w', pady=10)
        
#         # Buttons frame
#         buttons_frame = tk.Frame(self.dialog, bg='#2c3e50')
#         buttons_frame.pack(fill='x', padx=20, pady=10)
        
#         # Save button
#         save_btn = ttk.Button(
#             buttons_frame,
#             text="💾 Save",
#             command=self.save_settings
#         )
#         save_btn.pack(side='right', padx=5)
        
#         # Cancel button
#         cancel_btn = ttk.Button(
#             buttons_frame,
#             text="❌ Cancel",
#             command=self.dialog.destroy
#         )
#         cancel_btn.pack(side='right')
    
#     def save_settings(self):
#         """Save settings and close dialog"""
#         self.config.set("speech_rate", self.rate_var.get())
#         self.config.set("volume", self.volume_var.get())
#         self.config.set("auto_start", self.auto_start_var.get())
        
#         messagebox.showinfo("Settings", "Settings saved successfully!")
#         self.dialog.destroy()
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import logging
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class ModernVoiceAssistantGUI:
    def __init__(self, start_callback, stop_callback, talk_callback=None):
        self.config = Config()
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.talk_callback = talk_callback
        self.is_listening = False
        self.live_mode_active = False
        
        self.create_main_window()
        self.create_widgets()
        self.setup_styles()
        
        # Auto-start if configured
        if self.config.get("auto_start"):
            self.root.after(1000, self.start_listening)
    
    def create_main_window(self):
        """Create the main window with modern styling"""
        self.root = tk.Tk()
        self.root.title("Eight - Voice Assistant")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        self.root.configure(bg='#2c3e50')
        
        # Center window on screen
        self.center_window()
        
        # Configure window properties
        try:
            # You can add an icon file here
            # self.root.iconbitmap('icon.ico')
            pass
        except:
            pass
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_height()) // 2
        self.root.geometry(f"+{x}+{y}")
    
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Action.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=12)
        
        style.configure('Talk.TButton',
                       font=('Segoe UI', 10),
                       padding=8)
        
        style.configure('Quick.TButton',
                       font=('Segoe UI', 9),
                       padding=5)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🎙️ EIGHT Voice Assistant",
            font=('Segoe UI', 20, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
        # Status indicator
        self.status_frame = tk.Frame(self.root, bg='#2c3e50')
        self.status_frame.pack(fill='x', padx=20, pady=5)
        
        self.status_indicator = tk.Label(
            self.status_frame,
            text="●",
            font=('Arial', 20),
            fg='#e74c3c',  # Red when not listening
            bg='#2c3e50'
        )
        self.status_indicator.pack(side='left')
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to start",
            font=('Segoe UI', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        self.status_label.pack(side='left', padx=10)
        
        # Volume indicator
        self.volume_label = tk.Label(
            self.status_frame,
            text="🔊 Speak loudly for wake word",
            font=('Segoe UI', 10),
            fg='#f39c12',
            bg='#2c3e50'
        )
        self.volume_label.pack(side='right')
        
        # Control buttons frame
        controls_frame = tk.Frame(self.root, bg='#2c3e50')
        controls_frame.pack(fill='x', padx=20, pady=15)
        
        # Row 1: Main controls
        main_controls = tk.Frame(controls_frame, bg='#2c3e50')
        main_controls.pack(fill='x', pady=5)
        
        # Start/Stop button
        self.main_button = ttk.Button(
            main_controls,
            text="🎤 Start Wake Word Detection",
            command=self.toggle_listening,
            style='Action.TButton'
        )
        self.main_button.pack(side='left', padx=5)
        
        # Direct Talk button (NO WAKE WORD NEEDED)
        self.direct_talk_button = ttk.Button(
            main_controls,
            text="💬 Talk Directly (No Wake Word)",
            command=self.direct_talk,
            style='Action.TButton'
        )
        self.direct_talk_button.pack(side='left', padx=5)
        
        # Row 2: Live features
        live_controls = tk.Frame(controls_frame, bg='#2c3e50')
        live_controls.pack(fill='x', pady=5)
        
        # Live Talk button
        self.live_talk_button = ttk.Button(
            live_controls,
            text="🎙️ Start Live Chat",
            command=self.start_live_talk,
            style='Talk.TButton'
        )
        self.live_talk_button.pack(side='left', padx=5)
        
        # Text input for commands
        self.text_input_button = ttk.Button(
            live_controls,
            text="⌨️ Type Command",
            command=self.text_input_command,
            style='Talk.TButton'
        )
        self.text_input_button.pack(side='left', padx=5)
        
        # Settings button
        self.settings_button = ttk.Button(
            live_controls,
            text="⚙️ Settings",
            command=self.open_settings,
            style='Talk.TButton'
        )
        self.settings_button.pack(side='right', padx=5)
        
        # Volume test button
        self.volume_test_button = ttk.Button(
            live_controls,
            text="🔊 Test Microphone",
            command=self.test_microphone,
            style='Talk.TButton'
        )
        self.volume_test_button.pack(side='right', padx=5)
        
        # Conversation area
        conversation_frame = tk.LabelFrame(
            self.root,
            text="Conversation",
            font=('Segoe UI', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            relief='flat',
            padx=10,
            pady=10
        )
        conversation_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.text_area = scrolledtext.ScrolledText(
            conversation_frame,
            wrap=tk.WORD,
            width=70,
            height=18,
            font=('Consolas', 11),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='#ecf0f1',
            relief='flat',
            padx=10,
            pady=10
        )
        self.text_area.pack(fill='both', expand=True)
        
        # Quick actions frame
        actions_frame = tk.LabelFrame(
            self.root,
            text="Quick Actions (Work Instantly - No Wake Word)",
            font=('Segoe UI', 10, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            relief='flat'
        )
        actions_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Quick action buttons
        quick_buttons_frame1 = tk.Frame(actions_frame, bg='#34495e')
        quick_buttons_frame1.pack(fill='x', padx=5, pady=5)
        
        quick_buttons_frame2 = tk.Frame(actions_frame, bg='#34495e')
        quick_buttons_frame2.pack(fill='x', padx=5, pady=5)
        
        # First row of quick actions
        quick_actions1 = [
            ("🕐 Time", lambda: self.quick_command("what time is it")),
            ("📅 Date", lambda: self.quick_command("what's the date")),
            ("📺 YouTube", lambda: self.quick_command("open youtube")),
            ("🌐 Google", lambda: self.quick_command("open google")),
        ]
        
        # Second row of quick actions
        quick_actions2 = [
            ("🌦️ Weather", lambda: self.quick_command("weather")),
            ("📰 News", lambda: self.quick_command("latest news")),
            ("📸 Screenshot", lambda: self.quick_command("take screenshot")),
            ("💻 System Info", lambda: self.quick_command("system info")),
        ]
        
        for i, (text, command) in enumerate(quick_actions1):
            btn = ttk.Button(
                quick_buttons_frame1,
                text=text,
                command=command,
                style='Quick.TButton'
            )
            btn.pack(side='left', padx=3, fill='x', expand=True)
        
        for i, (text, command) in enumerate(quick_actions2):
            btn = ttk.Button(
                quick_buttons_frame2,
                text=text,
                command=command,
                style='Quick.TButton'
            )
            btn.pack(side='left', padx=3, fill='x', expand=True)
        
        # Add initial welcome message
        self.update_text("🎉 Welcome to Eight Voice Assistant!")
        self.update_text("=" * 60)
        self.update_text("✅ MULTIPLE WAYS TO INTERACT:")
        self.update_text("1. 🎤 Click 'Start Wake Word' then say 'EIGHT' loudly")
        self.update_text("2. 💬 Click 'Talk Directly' button (no wake word needed)")
        self.update_text("3. 🎙️ Click 'Start Live Chat' for AI conversation")
        self.update_text("4. ⌨️ Click 'Type Command' to type your requests")
        self.update_text("5. ⚡ Use Quick Action buttons below")
        self.update_text("=" * 60)
        self.update_text("🔊 If wake word doesn't work, use other methods!")
    
    def toggle_listening(self):
        """Toggle listening state"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start voice assistant"""
        try:
            self.is_listening = True
            self.main_button.configure(text="🛑 Stop Wake Word Detection")
            self.status_indicator.configure(fg='#27ae60')  # Green
            self.status_label.configure(text="Listening for 'EIGHT' wake word...")
            self.volume_label.configure(text="🔊 Say 'EIGHT' loudly!")
            
            # Run in separate thread
            threading.Thread(target=self.start_callback, daemon=True).start()
            
            self.update_text("🎤 Wake word detection started. Say 'EIGHT' loudly!")
            
        except Exception as e:
            self.update_text(f"❌ Error starting wake word detection: {str(e)}")
            logger.error(f"Start listening error: {e}")
    
    def stop_listening(self):
        """Stop voice assistant"""
        try:
            self.is_listening = False
            self.main_button.configure(text="🎤 Start Wake Word Detection")
            self.status_indicator.configure(fg='#e74c3c')  # Red
            self.status_label.configure(text="Wake word detection stopped")
            self.volume_label.configure(text="🔊 Click buttons to interact")
            
            self.stop_callback()
            self.update_text("🛑 Wake word detection stopped.")
            
        except Exception as e:
            self.update_text(f"❌ Error stopping: {str(e)}")
            logger.error(f"Stop listening error: {e}")
    
    def direct_talk(self):
        """Direct talk without wake word - MOST IMPORTANT FEATURE"""
        if self.talk_callback:
            try:
                self.update_text("🎙️ Direct talk mode - Listening now...")
                self.status_label.configure(text="Listening for direct command...")
                
                # Listen directly without wake word
                threading.Thread(
                    target=self._direct_listen_and_process,
                    daemon=True
                ).start()
                
            except Exception as e:
                self.update_text(f"❌ Error in direct talk: {str(e)}")
    
    def _direct_listen_and_process(self):
        """Listen and process command directly"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            self.update_text("🎧 Listening... Speak your command now!")
            
            with microphone as source:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            # Recognize speech
            command = recognizer.recognize_google(audio)
            self.update_text(f"👤 You said: {command}")
            
            # Process command directly
            self.talk_callback(command)
            
        except sr.WaitTimeoutError:
            self.update_text("⏰ Listening timeout - try again")
        except sr.UnknownValueError:
            self.update_text("❓ Could not understand - please try again")
        except Exception as e:
            self.update_text(f"❌ Direct talk error: {str(e)}")
        finally:
            self.status_label.configure(text="Ready for next command")
    
    def start_live_talk(self):
        """Start live conversation mode"""
        if self.live_mode_active:
            self.end_live_talk()
            return
            
        if self.talk_callback:
            try:
                self.update_text("🎙️ Starting live conversation mode...")
                self.live_talk_button.configure(text="🛑 End Live Chat")
                self.live_mode_active = True
                
                threading.Thread(
                    target=lambda: self.talk_callback("start live talk"),
                    daemon=True
                ).start()
            except Exception as e:
                self.update_text(f"❌ Error starting live chat: {str(e)}")
    
    def end_live_talk(self):
        """End live conversation mode"""
        if self.talk_callback:
            try:
                self.update_text("🛑 Ending live conversation mode...")
                self.live_talk_button.configure(text="🎙️ Start Live Chat")
                self.live_mode_active = False
                
                threading.Thread(
                    target=lambda: self.talk_callback("end live talk"),
                    daemon=True
                ).start()
            except Exception as e:
                self.update_text(f"❌ Error ending live chat: {str(e)}")
    
    def text_input_command(self):
        """Get command via text input"""
        try:
            command = simpledialog.askstring(
                "Type Command", 
                "Enter your command:\n(e.g., 'what time is it', 'open youtube', 'weather in London')",
                parent=self.root
            )
            
            if command:
                self.update_text(f"⌨️ Typed command: {command}")
                if self.talk_callback:
                    threading.Thread(
                        target=lambda: self.talk_callback(command),
                        daemon=True
                    ).start()
                    
        except Exception as e:
            self.update_text(f"❌ Text input error: {str(e)}")
    
    def test_microphone(self):
        """Test microphone volume levels"""
        try:
            self.update_text("🔊 Testing microphone - speak now for 5 seconds...")
            
            threading.Thread(target=self._test_mic_volume, daemon=True).start()
            
        except Exception as e:
            self.update_text(f"❌ Microphone test error: {str(e)}")
    
    def _test_mic_volume(self):
        """Test microphone volume levels"""
        try:
            import pyaudio
            import numpy as np
            
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024
            )
            
            max_volume = 0
            for i in range(50):  # 5 seconds at ~10 samples per second
                data = stream.read(1024, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.sqrt(np.mean(audio_data**2))
                max_volume = max(max_volume, volume)
                
                if i % 10 == 0:  # Update every second
                    self.update_text(f"🔊 Current volume: {volume:.0f}")
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            self.update_text(f"📊 Test complete! Max volume: {max_volume:.0f}")
            self.update_text(f"💡 Wake word threshold is 3000. Your max was {max_volume:.0f}")
            
            if max_volume < 1000:
                self.update_text("⚠️ Volume too low! Speak louder or use other interaction methods.")
            elif max_volume < 30:
                self.update_text("⚠️ Volume borderline. Try speaking louder for wake word.")
            else:
                self.update_text("✅ Volume good! Wake word should work.")
                
        except Exception as e:
            self.update_text(f"❌ Microphone test failed: {str(e)}")
    
    def quick_command(self, command):
        """Execute quick command"""
        if self.talk_callback:
            try:
                self.update_text(f"⚡ Quick command: {command}")
                threading.Thread(
                    target=lambda: self.talk_callback(command),
                    daemon=True
                ).start()
            except Exception as e:
                self.update_text(f"❌ Error executing command: {str(e)}")
    
    def open_settings(self):
        """Open settings dialog"""
        SettingsDialog(self.root, self.config)
    
    def update_text(self, text):
        """Update text area with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}\n"
        
        # Update in main thread
        self.root.after(0, self._update_text_safe, formatted_text)
    
    def _update_text_safe(self, text):
        """Thread-safe text update"""
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        
        # Keep only last 100 lines
        lines = self.text_area.get("1.0", tk.END).split('\n')
        if len(lines) > 100:
            self.text_area.delete("1.0", f"{len(lines)-100}.0")
    
    def run(self):
        """Start the GUI main loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop_listening()

class SettingsDialog:
    def __init__(self, parent, config):
        self.config = config
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("450x400")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#2c3e50')
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_settings_widgets()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 450) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 400) // 2
        self.dialog.geometry(f"+{x}+{y}")
    
    def create_settings_widgets(self):
        """Create settings widgets"""
        # Title
        title = tk.Label(
            self.dialog,
            text="⚙️ Assistant Settings",
            font=('Segoe UI', 16, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title.pack(pady=15)
        
        # Settings frame
        settings_frame = tk.Frame(self.dialog, bg='#2c3e50')
        settings_frame.pack(fill='both', expand=True, padx=20)
        
        # Wake word threshold
        tk.Label(
            settings_frame,
            text="Wake Word Volume Threshold:",
            fg='#ecf0f1',
            bg='#2c3e50',
            font=('Segoe UI', 10)
        ).pack(anchor='w', pady=(10, 5))
        
        self.threshold_var = tk.IntVar(value=self.config.get("wake_word_threshold", 0.6) * 5000)
        threshold_scale = tk.Scale(
            settings_frame,
            from_=1000,
            to=5000,
            orient='horizontal',
            variable=self.threshold_var,
            bg='#34495e',
            fg='#ecf0f1',
            highlightthickness=0,
            font=('Segoe UI', 9)
        )
        threshold_scale.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            settings_frame,
            text="Lower = more sensitive, Higher = less sensitive",
            fg='#95a5a6',
            bg='#2c3e50',
            font=('Segoe UI', 8)
        ).pack(anchor='w')
        
        # Speech rate
        tk.Label(
            settings_frame,
            text="Speech Rate:",
            fg='#ecf0f1',
            bg='#2c3e50',
            font=('Segoe UI', 10)
        ).pack(anchor='w', pady=(15, 5))
        
        self.rate_var = tk.IntVar(value=self.config.get("speech_rate"))
        rate_scale = tk.Scale(
            settings_frame,
            from_=100,
            to=300,
            orient='horizontal',
            variable=self.rate_var,
            bg='#34495e',
            fg='#ecf0f1',
            highlightthickness=0,
            font=('Segoe UI', 9)
        )
        rate_scale.pack(fill='x', pady=(0, 10))
        
        # Volume
        tk.Label(
            settings_frame,
            text="Volume:",
            fg='#ecf0f1',
            bg='#2c3e50',
            font=('Segoe UI', 10)
        ).pack(anchor='w', pady=(15, 5))
        
        self.volume_var = tk.DoubleVar(value=self.config.get("volume"))
        volume_scale = tk.Scale(
            settings_frame,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient='horizontal',
            variable=self.volume_var,
            bg='#34495e',
            fg='#ecf0f1',
            highlightthickness=0,
            font=('Segoe UI', 9)
        )
        volume_scale.pack(fill='x', pady=(0, 10))
        
        # Auto-start checkbox
        self.auto_start_var = tk.BooleanVar(value=self.config.get("auto_start"))
        auto_start_check = tk.Checkbutton(
            settings_frame,
            text="Auto-start wake word detection",
            variable=self.auto_start_var,
            fg='#ecf0f1',
            bg='#2c3e50',
            selectcolor='#34495e',
            font=('Segoe UI', 10)
        )
        auto_start_check.pack(anchor='w', pady=15)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.dialog, bg='#2c3e50')
        buttons_frame.pack(fill='x', padx=20, pady=15)
        
        # Test microphone button
        test_btn = ttk.Button(
            buttons_frame,
            text="🔊 Test Mic",
            command=self.test_settings
        )
        test_btn.pack(side='left', padx=5)
        
        # Save button
        save_btn = ttk.Button(
            buttons_frame,
            text="💾 Save",
            command=self.save_settings
        )
        save_btn.pack(side='right', padx=5)
        
        # Cancel button
        cancel_btn = ttk.Button(
            buttons_frame,
            text="❌ Cancel",
            command=self.dialog.destroy
        )
        cancel_btn.pack(side='right')
    
    def test_settings(self):
        """Test current settings"""
        threshold = self.threshold_var.get()
        messagebox.showinfo("Settings", f"Current threshold: {threshold}\nSpeak loudly to test if your voice exceeds this level.")
    
    def save_settings(self):
        """Save settings and close dialog"""
        self.config.set("wake_word_threshold", self.threshold_var.get() / 5000.0)
        self.config.set("speech_rate", self.rate_var.get())
        self.config.set("volume", self.volume_var.get())
        self.config.set("auto_start", self.auto_start_var.get())
        
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.dialog.destroy()
3000