Cube
====

Basic Operations
----------------

- New Cube
- Delete Cube
- Cube Tags
- View Cube
- Fav Cube
- Unfav Cube

Basic Classes
-------------


ThingConfig

Thing

ThingSite

ThingForm

ThingUI
  - ThingModel

ThingSiteUI
  - ThingSiteModel
  - ThingModel


URL Patterns
------------

/c/thing *
/c/thing/new *
/c/thing/tags *
/c/thing/id *
/c/thing/id/edit *
/c/thing/id/delete
/c/thing/id/want
/c/thing/id/rank
/c/thing/id/have
/c/thing/id/cancel
/c/thing/id/comment
/c/thing/id/article *
/c/thing/id/fans *
  
  
App layout
----------

cube
  models
  views
  templates
  
  things
    book
      models
      views
      templates
    movie

Cube Config
-----------

Cube:
 - cube_type
 - url:'book'
 - name: 'Book'
 - tags {

     }
 - views: {
      new: view('New'),
      want: view('Want'),
      have: view('Have'),
      rank: view('Rank'),
      comment: view('')
    }
 - fields:{
       photo: field('Photo')
       name: field('Name')
     }
 - names:{

    }