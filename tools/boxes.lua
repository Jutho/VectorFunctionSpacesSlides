-- Numbered boxes for definitions, theorems, examples, ... in the style of the lecture notes.
--
--   ::: {.definitie nr="4.2" title="Norm"}
--   Een norm is ...
--   :::
--
-- becomes a <div class="vfr-box vfr-definitie"> whose text starts with a bold
-- "Definitie 4.2 (Norm)." in the colour of the box (styles in tools/boxes.css).
-- `nr` is the number of the environment in the notes (built without `advanced`); leave it
-- out for statements that have no counterpart there. `title` is optional.

local names = {
  definitie = "Definitie", stelling = "Stelling", propositie = "Propositie",
  lemma = "Lemma", gevolg = "Gevolg", voorbeeld = "Voorbeeld",
  opmerking = "Opmerking", bewijs = "Bewijs",
}

function Div(div)
  local kind
  for _, c in ipairs(div.classes) do
    if names[c] then kind = c end
  end
  if not kind then return nil end

  local label = names[kind]
  if div.attributes.nr then label = label .. " " .. div.attributes.nr end
  local inlines = { pandoc.Str(label) }
  if div.attributes.title then
    inlines = { pandoc.Str(label), pandoc.Space(),
                pandoc.Str("(" .. div.attributes.title .. ")") }
  end
  table.insert(inlines, pandoc.Str("."))
  local head = pandoc.Span({ pandoc.Strong(inlines) }, { class = "vfr-box-label" })

  local first = div.content[1]
  if first and (first.t == "Para" or first.t == "Plain") then
    first.content:insert(1, pandoc.Space())
    first.content:insert(1, head)
  else
    -- a block of its own: reveal.js makes lists inline-blocks, which would sit next to a bare label
    div.content:insert(1, pandoc.Para({ head }))
  end

  div.classes = pandoc.List({ "vfr-box", "vfr-" .. kind })
  div.attributes.nr = nil
  div.attributes.title = nil
  return div
end
