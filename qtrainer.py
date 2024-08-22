import tensorflow

class qtrainer():
    def __init__(self,model,learningrate = 1e-4,gamma = 0.9):
        self.model = model
        self.gamma = gamma
        self.optimizer = tensorflow.keras.optimizers.Adam(learning_rate = learningrate)
        self.loss_object = tensorflow.keras.losses.MeanSquaredError()

    @tensorflow.function
    def train_step(self,states,actions,rewards,nextstates,dones):
        futurerewards = tensorflow.reduce_max(self.model(nextstates),axis = 1)
        #q value = reward + discount factor * expeted future
        updatedqval = rewards + tensorflow.math.multiply(self.gamma,futurerewards)
        updatedqval = tensorflow.math.multiply(updatedqval,(1 - dones))
        masks = actions
        with tensorflow.GradientTape() as tape:
            qvalues = self.model(states)
            qaction = tensorflow.reduce_sum(tensorflow.multiply(qvalues,masks), axis = 1)
            loss = self.loss_object(updatedqval,qaction)
            grads = tape.gradient(loss,self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(grads,self.model.trainable_variables))