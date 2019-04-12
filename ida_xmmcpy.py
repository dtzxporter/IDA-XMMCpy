import idaapi
import idautils
import idc
import operator


class Kp_Menu_Context(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    @classmethod
    def get_name(self):
        return self.__name__

    @classmethod
    def get_label(self):
        return self.label

    @classmethod
    def register(self, plugin, label):
        self.plugin = plugin
        self.label = label
        instance = self()
        return idaapi.register_action(idaapi.action_desc_t(
            self.get_name(),  # Name. Acts as an ID. Must be unique.
            instance.get_label(),  # Label. That's what users see.
            instance  # Handler. Called when activated, and for updating
        ))

    @classmethod
    def unregister(self):
        """Unregister the action.
        After unregistering the class cannot be used.
        """
        idaapi.unregister_action(self.get_name())

    @classmethod
    def activate(self, ctx):
        # dummy method
        return 1

    @classmethod
    def update(self, ctx):
        if ctx.form_type == idaapi.BWN_DISASM:
            return idaapi.AST_ENABLE_FOR_FORM
        return idaapi.AST_DISABLE_FOR_FORM


class Exporter(Kp_Menu_Context):
    def activate(self, ctx):
        self.plugin.export_xmm()
        return 1


p_initialized = False


class IDAXMMCpy_Plugin_t(idaapi.plugin_t):
    comment = "XMMCpy plugin for IDA Pro"
    help = "todo"
    wanted_name = "XMMCpy"
    wanted_hotkey = "Ctrl-Alt-E"
    flags = idaapi.PLUGIN_KEEP

    def init(self):
        global p_initialized

        try:
            Exporter.register(self, "XMMCpy")
        except:
            pass

        if p_initialized is False:
            p_initialized = True
            idaapi.register_action(idaapi.action_desc_t(
                "XMMCpy",
                "Export XMMWORDs to C++",
                self.export_xmm,
                None,
                None,
                0
            ))
            idaapi.attach_action_to_menu(
                "Edit/XMMCpy", "XMMCpy", idaapi.SETMENU_APP)

        return idaapi.PLUGIN_KEEP

    def term(self):
        pass

    def run(self, arg):
        self.export_xmm()

    def export_xmm(self):
        print("%x" % get_screen_ea())


def PLUGIN_ENTRY():
    return IDAXMMCpy_Plugin_t()
