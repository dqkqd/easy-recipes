class ResizeObserver {
  callback?: ResizeObserverCallback;

  constructor(callback: ResizeObserverCallback) {
    this.callback = callback;
  }

  observe() {
    this.callback?.([], this);
  }

  unobserve() {
    this.callback = undefined;
  }

  disconnect() {
    this.callback = undefined;
  }
}

(global as any).ResizeObserver = ResizeObserver;
(global as any).CSS = { supports: () => false };
