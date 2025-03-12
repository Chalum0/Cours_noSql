# NoSQL with MongoDB
Database used : [Comptage des voyageurs montants dans les trains Transilien](https://ressources.data.sncf.com/explore/dataset/comptage-voyageurs-trains-transilien/information/)

## NoSQL vs SGBDR
Une base de données NoSQL ne contient pas de colones mais des champs qu'il est possible de modifier bien plus facilement qu'en SQL. Il est facile d'ajouter des champs dans un document.

Les frameworks utilisent généralement des ORM qui permettent de gérer l'évolution du schéma via des migrations. Ils permettent de garantir la cohérence des données.

Dans un SGBDR, l’évolution du schéma est rigide et nécessite des migrations gérées par des outils dédiés. En MongoDB, le schéma est flexible et permet d’ajouter ou modifier des champs dynamiquement, mais sans contrôle strict, ce qui peut entraîner des incohérences. Pour éviter cela, il est recommandé d’assurer la rétrocompatibilité, de prévoir des valeurs par défaut, d’utiliser des validations de schéma et de structurer l’évolution des documents avec des scripts de mise à jour.
