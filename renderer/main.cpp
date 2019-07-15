#include <Eigen/Core>
#include "Environment.h"

int main(){

	ICC::Environment *env = new ICC::Environment();
	Eigen::VectorXd state = env->getState();
	Eigen::VectorXd action = state;
	env->setAction(action);
	env->step();
	env->getReward();

	return 0;
}