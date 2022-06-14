require 'squib'

Squib::Deck.new(cards: 2) do
  background color: 'white'
  text str: ['Hello', 'World!']
  save_png prefix: 'basic_'
end
