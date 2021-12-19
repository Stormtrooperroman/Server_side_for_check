from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
import re

def main(files):
    
    layer = get_channel_layer()
    async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"new_file","message": f"Start scaning...",})
    for file_name, file in files.items():

        async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"new_file","message": f"Start scaning file '{file_name}'...",})

        p = re.compile("unsafe\s+fn\s")
        names = {}
        for m in p.finditer(file):    
            
            name = (re.sub("[^a-zA-Z1-9_]", "", file[m.end()::].split()[0]))
            names[name]=m.end()
            async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"warning","message": f"Warning: Setting an unsafe function '{name}' to a position {m.start()}!",})

        for name, val in names.items():
            p = re.compile(f"\s*{name}\s*\(")
            for m in p.finditer(file):
                
                if(val-1!=m.start()):
                    async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"danger","message": f"Danger: Calling  an unsafe function '{name}' at a position {m.start()}!",})
        names.clear()
        names = {}
        p = re.compile("unsafe\s+trait\s")
        for m in p.finditer(file):    
            
            name = (re.sub("[^a-zA-Z1-9_]", "", file[m.end()::].split()[0]))
            names[name]=m.end()
            async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"warning","message": f"Warning: Setting an unsafe trait '{name}' to a position {m.start()}!",})

        for name, val in names.items():
            p = re.compile(f"unsafe\s+impl\s+{name}\s+")
            for m in p.finditer(file):
                
                if(val-1!=m.start()):
                    async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"danger","message": f"Danger: Calling  an unsafe trait '{name}' at a position {m.start()}!",})
        
        names.clear()
        names = {}
        p = re.compile("as\s+\*const\s")
        for m in p.finditer(file):    
            
            name = (re.sub("[^a-zA-Z1-9_]", " ", file[:m.start()-1:])).split()[-2]
            names[name]=m.end()
            async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"warning","message": f"Warning: Creating raw pointer '{name}' to a position {m.start()}!",})

        p = re.compile("as\s+\*mut\s")
        for m in p.finditer(file):    
            
            name = (re.sub("[^a-zA-Z1-9_]", " ", file[:m.start()-1:])).split()[-2]
            names[name]=m.end()
            async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"warning","message": f"Warning: Creating raw pointer '{name}' to a position {m.start()}!",})


        for name, val in names.items():
            p = re.compile(f"\*{name}\W")
            for m in p.finditer(file):
                
                if(val-1!=m.start()):
                    async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"danger","message": f"Danger: Dereferencing a Raw Pointer '{name}' at a position {m.start()}!",})

        names.clear()
        names = {}
        p = re.compile("static\s+mut\s")
        for m in p.finditer(file):    
            name = (re.sub("[^a-zA-Z1-9_]", " ", file[m.end()::])).split()[0]
            names[name]=m.end()
            async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"warning","message": f"Warning: Using a Mutable Static Variable '{name}' at  position {m.start()}!",})

        for name, val in names.items():
            p = re.compile(f"\W*{name}\W")
            for m in p.finditer(file):
                
                if(val-1!=m.start()):
                    async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"danger","message": f"Danger: Accessing or Modifying a Mutable Static Variable '{name}' at a position {m.start()}!",})

        async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"new_file","message": f"End scaning file '{file_name}'...",})
    async_to_sync(layer.group_send)("hello", {"type": "chat.message", "status":"new_file","message": f"End scaning...",})