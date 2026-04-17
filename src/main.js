const slint = require("slint-ui");
const ServerManager = require("./server-manager");

const { MainWindow } = slint.loadFile(__dirname + "/ui.slint");
const { AboutDialog } = slint.loadFile(__dirname + "/about-dialog.slint");
const { ConfigDialog } = slint.loadFile(__dirname + "/config-dialog.slint");

const mainWindow = new MainWindow();
const serverManager = new ServerManager();

const refreshStatus = () => {
    const text = serverManager.getStatusText();
    mainWindow.statusText = text;
    mainWindow.statusColor = text.startsWith("Running") ? "#2ecc71" : "#000000";
};

refreshStatus();

mainWindow.startServer = () => {
    console.log("Start Server clicked");
    mainWindow.statusText = "Starting...";
    mainWindow.statusColor = "#f39c12";
    serverManager
        .start()
        .then((r) => {
            console.log(r.message);
            if (r.success) {
                mainWindow.statusText = `Running on ${serverManager.config.port}`;
                mainWindow.statusColor = "#2ecc71";
            } else {
                refreshStatus();
            }
        })
        .catch((e) => {
            console.error(e);
            refreshStatus();
        });
};

mainWindow.stopServer = () => {
    console.log("Stop Server clicked");
    mainWindow.statusText = "Stopping...";
    mainWindow.statusColor = "#f39c12";
    const r = serverManager.stop();
    console.log(r.message);
    refreshStatus();
};

mainWindow.syncSessions = () => {
    console.log("Sync Sessions clicked");
    mainWindow.statusText = "Syncing...";
    mainWindow.statusColor = "#f39c12";
    serverManager
        .sync()
        .then((r) => console.log(r.message))
        .catch((e) => console.error(e))
        .finally(refreshStatus);
};

mainWindow.configuration = async () => {
    console.log("Configuration clicked");

    const dlg = new ConfigDialog();
    dlg.portText = serverManager.config.port;
    dlg.commandText = serverManager.config.command;
    dlg.directoryText = serverManager.config.directory;

    dlg.saveConfig = async (port, command, directory) => {
        console.log(`Saving config: port=${port}, command=${command}, directory=${directory}`);
        serverManager.updateConfig({ port, command, directory });

        // Check if server is running and restart it with new config
        if (serverManager.isRunning()) {
            console.log("Server is running, restarting with new config...");
            mainWindow.statusText = "Restarting...";
            mainWindow.statusColor = "#f39c12";

            const stopResult = serverManager.stop();
            console.log("Stop result:", stopResult.message);

            // Wait a moment for clean shutdown
            await new Promise(resolve => setTimeout(resolve, 1000));

            const startResult = await serverManager.start();
            console.log("Start result:", startResult.message);

            refreshStatus();
        } else {
            console.log("Server is not running, no restart needed");
            refreshStatus();
        }
    };

    dlg.closeDialog = () => {
        dlg.hide();
    };

    dlg.show();
};

mainWindow.about = () => {
    console.log("About clicked");

    const dlg = new AboutDialog();
    dlg.closeDialog = () => {
        dlg.hide();
    };
    dlg.show();
};

mainWindow.quit = () => {
    console.log("Quit clicked");
    slint.quitEventLoop();
    process.exit(0);
};

mainWindow.show();
slint.runEventLoop();
