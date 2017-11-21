# DecideViz

Online debate tools in participatory democracy and crowdsourcing legislation remains limited by several factors. One of them arises when discussion of proposals reach a large number of contributions and therefore citizens encounter 
difficulties in mapping the arguments that constitute the dialectical debate. 

To address this issue, this visualization tool shows the discussion of a debate/proposal. The tool builds on *[Decide Madrid](https://decide.madrid.es/)*, the platform for direct democracy launched by the City Council of Madrid in September 2015. Discussions are visualized hierarchically as an interactive radial tree in which the root node corresponds to the proposal and the rest of the nodes correspond to the comments from the users. To highlight the arborescence of the discussion and to distinguish the arguments of every branch of the thread, the tool applies a flexible force-directed graph layout that accelerates charge interaction through the Barnes-Hut approximation. In addition, to identify the messages that receive more attention, the tree layout of the discussion includes additional information, such as positive or negative votes that are associated with individual comments.
The size and colour of the nodes is determined according to the number of votes and the ratio of positive/negative votes, respectively:
* Black: Root (proposal)
* Grey: Comment with no votes
* Green (scale): Comment with majority of positive votes
* Red (scale): Comment with majority of negative votes
* Orange: Comment with no strong preference of positive or negative votes

The visualization also includes an informative panel with the description of the tool and the metadata of a node (author, message, date and positive/negative votes) when the user rolls the mouse over it. 

More info about this tool can be found at the D-CENT deliverable: [From Citizen Data to Wisdom of the Crowd](http://dcentproject.eu/wp-content/uploads/2016/01/D2.4-%EF%BF%BCFrom-citizen-data-to-wisdom-of-the-Crowd.pdf
) 


![alt text](https://elaragon.files.wordpress.com/2016/03/proposal.png)

## How to use it

The tool requires the following python packages:
* bottle
* BeautifulSoup
* urllib
* re
* json

Then run the app locally:

```
python app.py 
```

Finally explore debates and proposals in a web browser by setting the type (debates/proposals) and the corresponding numerical ID , e.g.:
```
http://localhost:8080/thread/?id=4230&type=debates
http://localhost:8080/thread/?id=417&type=proposal
```

## License
Code published under AFFERO GPL v3 (see [LICENSE-AGPLv3.txt](https://www.gnu.org/licenses/agpl.txt))


## Acknowledgments
This work is supported by the EU project [D-CENT](http://dcentproject.eu/) (FP7/CAPS 610349) and the Spanish Ministry of Economy and Competitiveness under the [María de Maeztu Units of Excellence Programme](https://www.upf.edu/icaria-cei/en/news/1027.html) (MDM-2015-0502) 

