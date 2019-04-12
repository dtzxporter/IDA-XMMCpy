import idaapi
import idautils
import idc
import operator

if idaapi.IDA_SDK_VERSION >= 690:
    from PyQt5.Qt import QApplication
else:
    from PySide.QtGui import QApplication


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
        self.plugin.export_xmm_float()
        return 1


p_initialized = False


class IDAXMMCpyFt_Plugin_t(idaapi.plugin_t):
    comment = "XMMCpy (Float) plugin for IDA Pro"
    help = "todo"
    wanted_name = "XMMCpy (Float)"
    wanted_hotkey = "Ctrl-Shift-F"
    flags = idaapi.PLUGIN_KEEP

    def init(self):
        
        try:
            Exporter.register(self, "XMMCpy (Float)")
        except:
            pass

        return idaapi.PLUGIN_KEEP

    def term(self):
        pass

    def run(self, arg):
        self.export_xmm_float()

    def export_xmm_float(self):
        result_float = "_mm_set_ps(%f, %f, %f, %f)" % (idc.GetFloat(get_screen_ea() + 12),
                                                            idc.GetFloat(get_screen_ea() + 8), idc.GetFloat(get_screen_ea() + 4), idc.GetFloat(get_screen_ea()))
        print("XMMCpy (Float) Result: %s" % result_float)
        QApplication.clipboard().setText(result_float)


def PLUGIN_ENTRY():
    return IDAXMMCpyFt_Plugin_t()
