
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'L', 'R', 'T']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    json_data = request.json
    logger.info(json_data)

    state = json_data["arena"]["state"]
    self_name = json_data["_links"]["self"]["href"]
    logger.info(self_name)
    logger.info(state[self_name])

    pos = []
    for _, val in state.items():
        pos.append((val['x'], val['y']))
    logger.info(pos)

    if state[self_name]["wasHit"]:
        return moves[random.randrange(len(moves) - 1)]

    # get 3x3 people
    my_pos = (state[self_name]['x'], state[self_name]['y'])
    neighbors = [p for p in pos if abs(p[0] - my_pos[0]) <= 3 and abs(p[1] - my_pos[1]) <=3 ]
    logger.info(neighbors)

    if state[self_name]["direction"] == "N":
        if any([p[0] == my_pos[0] and p[1] > my_pos[1] for p in neighbors]):
            return 'T'
    if state[self_name]["direction"] == "S":
        if any([p[0] == my_pos[0] and p[1] < my_pos[1] for p in neighbors]):
            return "T"
    if state[self_name]["direction"] == "W":
        if any([p[1] == my_pos[1] and p[0] < my_pos[0] for p in neighbors]):
            return "T"
    if state[self_name]["direction"] == "E":
        if any([p[1] == my_pos[1] and p[0] > my_pos[0] for p in neighbors]):
            return "T"

    return moves[random.randrange(len(moves) - 1)]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
