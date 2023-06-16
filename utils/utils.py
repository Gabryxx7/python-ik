import json
class Utils:
  @staticmethod
  def dict_str(data):
    data_str = ""
    try:
      data_str = json.dumps(data, indent=2, skipkeys=True)
      # print(data_str)
    except Exception as e:
      data_str = f"Exception printing dict: {e}"
    return data_str