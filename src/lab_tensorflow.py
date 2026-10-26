"""LAB3: real TensorFlow CPU benchmark, stratified train/validation/test."""
import os,time
os.environ['TF_DETERMINISTIC_OPS']='1';os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import numpy as np,pandas as pd,tensorflow as tf
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,log_loss
from common import project,save,environment,configure_plot
P=project('LAB3_tensorflow')
def main():
 tf.config.threading.set_intra_op_parallelism_threads(2);tf.config.threading.set_inter_op_parallelism_threads(2)
 data=load_digits();X=data.data.astype('float32')/16;y=data.target;ids=np.arange(len(y))
 tr,rest=train_test_split(ids,test_size=.4,stratify=y,random_state=42);va,te=train_test_split(rest,test_size=.5,stratify=y[rest],random_state=42)
 assert not set(tr)&set(va) and not set(tr)&set(te) and not set(va)&set(te)
 baseline=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,C=1));t=time.perf_counter();baseline.fit(X[tr],y[tr]);bt=time.perf_counter()-t
 bp=baseline.predict_proba(X[te]);bv=baseline.predict_proba(X[va]);results=[];histories=[]
 for seed in [42,43,44]:
  tf.keras.backend.clear_session();tf.keras.utils.set_random_seed(seed)
  model=tf.keras.Sequential([tf.keras.layers.Input((64,)),tf.keras.layers.Dense(64,activation='relu'),tf.keras.layers.Dropout(.2),tf.keras.layers.Dense(32,activation='relu'),tf.keras.layers.Dense(10,activation='softmax')])
  model.compile(optimizer=tf.keras.optimizers.Adam(.001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
  t=time.perf_counter();history=model.fit(X[tr],y[tr],validation_data=(X[va],y[va]),epochs=60,batch_size=64,verbose=0,callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss',patience=6,restore_best_weights=True)]);seconds=time.perf_counter()-t
  prob=model.predict(X[te],verbose=0);v=model.predict(X[va],verbose=0)
  row={'seed':seed,'epochs':len(history.history['loss']),'parameters':int(model.count_params()),'fit_seconds':seconds,'test_accuracy':float(accuracy_score(y[te],prob.argmax(axis=1))),'test_macro_f1':float(f1_score(y[te],prob.argmax(axis=1),average='macro')),'test_log_loss':float(log_loss(y[te],prob)),'validation_accuracy':float(accuracy_score(y[va],v.argmax(axis=1))),'final_train_accuracy':float(history.history['accuracy'][-1]),'final_validation_accuracy':float(history.history['val_accuracy'][-1])};results.append(row)
  histories.append(pd.DataFrame(history.history).assign(epoch=np.arange(1,len(history.history['loss'])+1),seed=seed))
 pd.concat(histories).to_csv(P/'results/learning_history.csv',index=False)
 # Recommendation uses validation only, including an explicit 1 percentage point complexity hurdle.
 network_val=float(np.mean([x['validation_accuracy'] for x in results]));baseline_val=float(accuracy_score(y[va],bv.argmax(axis=1)));retained='tensorflow_mlp' if network_val>=baseline_val+.01 else 'logistic_regression'
 save(P/'results/metrics.json',{'dataset':'sklearn bundled UCI optical digits, 1797 8x8 images; original UCI optical recognition donation; non-overlapping random stratified sample split, not writer-disjoint','source':'https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html','split_sizes':{'train':len(tr),'validation':len(va),'test':len(te)},'split_seed':42,'baseline':{'fit_seconds':bt,'validation_accuracy':baseline_val,'test_accuracy':float(accuracy_score(y[te],bp.argmax(axis=1))),'test_macro_f1':float(f1_score(y[te],bp.argmax(axis=1),average='macro')),'test_log_loss':float(log_loss(y[te],bp))},'tensorflow_runs':results,'validation_mean_network_accuracy':network_val,'decision_rule':'Retain MLP only if mean validation accuracy across 3 initialisation seeds >= baseline +0.01; test does not select model','retained':retained,'limits':['Small image benchmark, not an industrial deployment.','Same split across seeds: measures initialization variability, not independent test replication.','No writer identifiers; writer leakage cannot be excluded.'],'environment':environment()})
 plt=configure_plot();fig,ax=plt.subplots();h=histories[0];ax.plot(h.epoch,h.loss,label='Training loss');ax.plot(h.epoch,h.val_loss,label='Validation loss');ax.set(xlabel='Epoch',ylabel='Cross-entropy',title='TensorFlow MLP: seed 42 learning curve');ax.legend();fig.savefig(P/'figures/learning.png');plt.close(fig)
 print('LAB3 baseline',float(accuracy_score(y[te],bp.argmax(axis=1))),'retained',retained,flush=True)
if __name__=='__main__':main()
