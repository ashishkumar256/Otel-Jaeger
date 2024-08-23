import { NodeSDK } from '@opentelemetry/sdk-node';
import * as process from 'process'; 
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { AsyncHooksContextManager } from '@opentelemetry/context-async-hooks';
import * as api from '@opentelemetry/api'; 

const contextManager = new AsyncHooksContextManager().enable();
api.context.setGlobalContextManager(contextManager);

export const otelSDK = new NodeSDK({
  instrumentations: [
    getNodeAutoInstrumentations(),
  ],
});

process.on('SIGTERM', () => {
  otelSDK
    .shutdown()
    .then(
      () => console.log('Shut down successfully'),
      (err) => console.log('Error shutting down ', err),
    )
    .finally(() => process.exit(0));
});
