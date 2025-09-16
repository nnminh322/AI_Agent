from agents.state import MessageState
import yaml

with open("./configs/config.yaml", "r") as f:
    db_config = yaml.safe_load(f)["database"]

n_retry_max = db_config["num_retry"]
dialect = db_config["DIALECT"]


with open("./documents/base_prompt_template.txt", "r") as f:
    base_prompt = f.read()

with open("./documents/retry_prompt_template.txt") as f:
    retry_prompt = f.read()


def sys_msg_node(state: MessageState) -> MessageState:
    base_sys_msg = base_prompt.replace("DIALECT", dialect)
    if state["SQL_num_retry"] == 0:
        state["system_msg"] = base_sys_msg
        return state
    else:
        retry_sys_msg = retry_prompt.replace("state['SQL_num_retry']", state["SQL_num_retry"])
        retry_sys_msg = retry_sys_msg.replace("state['SQL_error_results']", state["SQL_error_results"])
        state["system_msg"] = base_sys_msg + retry_sys_msg
        return state