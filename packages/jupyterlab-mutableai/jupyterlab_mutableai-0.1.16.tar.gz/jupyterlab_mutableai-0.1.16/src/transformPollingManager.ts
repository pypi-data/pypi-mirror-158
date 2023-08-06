import { JupyterFrontEnd } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { PromiseDelegate } from '@lumino/coreutils';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { requestAPI } from './handler';
import { CodeViewerWidget } from './widgets/CodeViewer';
import { notebookIcon } from '@jupyterlab/ui-components';

interface ITransformPollingManagerProps {
  docManager: IDocumentManager;
  app: JupyterFrontEnd;
  getSettings: () => Promise<ISettingRegistry.ISettings>;
}
interface ICheckStatusResponse {
  status: string;
  file: string;
}

interface IFileChangeResponse {
  status: string;
}

export class TransformPollingManager {
  constructor(props: ITransformPollingManagerProps) {
    this._docManager = props.docManager;
    this._app = props.app;

    props
      .getSettings()
      .then(mutableAI => {
        this._mutableAI = mutableAI;
        this._ready.resolve();
      })
      .catch(reason => {
        console.warn(reason);
        this._ready.reject(reason);
      });

    this._count = 0;
    this._file_path = '';

    this.startPolling = this.startPolling.bind(this);
    this.acceptFile = this.acceptFile.bind(this);
    this.declineFile = this.declineFile.bind(this);
  }

  /**
   * A promise that resolves when the settings have been loaded.
   */
  get ready(): Promise<void> {
    return this._ready.promise;
  }

  async startPolling(
    file_path: string,
    current_file_path: string
  ): Promise<void> {
    this._file_path = file_path;
    this._current_file_path = current_file_path;

    const dataToSend = { file_path };

    const pollingRef = setInterval(async () => {
      this._count += 1;
      try {
        const response: ICheckStatusResponse = await requestAPI<any>(
          'CHECK_STATUS',
          {
            body: JSON.stringify(dataToSend),
            method: 'POST'
          }
        );

        if (response?.status === 'finished') {
          // Open transformed file here.

          const close = () => this._app.shell.currentWidget?.close();
          const content = new CodeViewerWidget(
            close,
            response.file,
            this._app,
            {
              onAcceptChanges: this.acceptFile,
              onDeclineChanges: this.declineFile
            }
          );
          const widget = new MainAreaWidget<CodeViewerWidget>({ content });
          widget.title.label = 'MutableAI Code Viewer';
          widget.title.icon = notebookIcon;
          this._app.shell.add(widget, 'main', { mode: 'split-right' });
          clearInterval(pollingRef);
        } else {
          if (this._count >= 60) {
            this._count = 0;
            this._file_path = '';
            clearInterval(pollingRef);
          }
        }
      } catch (error) {
        console.log('Failed to make request. Reason: ' + error.toString());
      }
    }, 1000);
  }

  acceptFile() {
    const apiKey = this._mutableAI?.get('apiKey').composite as string;
    const transformDomain = this._mutableAI?.get('transformDomain')
      .composite as string;

    const dataToSend = {
      file_path: this._file_path,
      current_file_path: this._current_file_path,
      url: transformDomain,
      action: 'accept',
      apiKey
    };

    const reply = requestAPI<any>('FILE_ACTION', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });

    reply
      .then((response: IFileChangeResponse) => {
        if (response.status === 'completed') {
          console.log('File accepted.');
          const widgets = this._app.shell.widgets('main');
          while (true) {
            const widget = widgets.next();
            if (widget) {
              widget.close();
            } else {
              break;
            }
          }
          setTimeout(() => {
            this._docManager.open(this._current_file_path);
            const launcher = this._app.shell.widgets('main').next();

            if (launcher?.title.label === 'Launcher') {
              setTimeout(() => {
                launcher.close();
              }, 300);
            }
          }, 300);
        } else {
          console.log('File accepting failed.');
        }
      })
      .catch(e => console.log('File accepting failed.', e));
  }

  declineFile() {
    const apiKey = this._mutableAI?.get('apiKey').composite as string;
    const transformDomain = this._mutableAI?.get('transformDomain')
      .composite as string;

    const dataToSend = {
      file_path: this._file_path,
      current_file_path: this._current_file_path,
      action: 'decline',
      url: transformDomain,
      apiKey
    };

    const reply = requestAPI<any>('FILE_ACTION', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });

    reply
      .then((response: IFileChangeResponse) => {
        if (response.status === 'completed') {
          console.log('File decline.');
          const widgets = this._app.shell.widgets('main');
          while (true) {
            const widget = widgets.next();
            if (widget) {
              if (widget.title.label === 'MutableAI Code Viewer') {
                widget.close();
              }
            } else {
              break;
            }
          }
        } else {
          console.log('File declining failed.');
        }
      })
      .catch(e => console.log('File declining failed.', e));
  }

  private _docManager: IDocumentManager;
  private _app: JupyterFrontEnd;
  private _ready = new PromiseDelegate<void>();
  private _mutableAI: ISettingRegistry.ISettings | null = null;
  private _count: number = 0;
  private _file_path: string = '';
  private _current_file_path: string = '';
}
