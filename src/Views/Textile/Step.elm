module Views.Textile.Step exposing (view)

import Autocomplete exposing (Autocomplete)
import Data.AutocompleteSelector as AutocompleteSelector
import Data.Country as Country
import Data.Dataset as Dataset
import Data.Env as Env
import Data.Gitbook as Gitbook
import Data.Impact as Impact exposing (noComplementsImpacts)
import Data.Impact.Definition as Definition exposing (Definition)
import Data.Scope as Scope
import Data.Split as Split exposing (Split)
import Data.Textile.DyeingMedium as DyeingMedium exposing (DyeingMedium)
import Data.Textile.Fabric as Fabric exposing (Fabric)
import Data.Textile.Formula as Formula
import Data.Textile.Inputs as Inputs exposing (Inputs)
import Data.Textile.MakingComplexity as MakingComplexity exposing (MakingComplexity)
import Data.Textile.Material as Material exposing (Material)
import Data.Textile.Material.Origin as Origin
import Data.Textile.Material.Spinning as Spinning exposing (Spinning)
import Data.Textile.Printing as Printing exposing (Printing)
import Data.Textile.Query exposing (MaterialQuery)
import Data.Textile.Simulator exposing (stepMaterialImpacts)
import Data.Textile.Step as Step exposing (Step)
import Data.Textile.Step.Label as Label exposing (Label)
import Data.Textile.WellKnown as WellKnown
import Data.Transport as Transport
import Data.Unit as Unit
import Duration exposing (Duration)
import Energy
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Mass exposing (Mass)
import Quantity
import Route
import Static.Db exposing (Db)
import Views.BaseElement as BaseElement
import Views.Button as Button
import Views.ComplementsDetails as ComplementsDetails
import Views.Component.SplitInput as SplitInput
import Views.Component.StepsBorder as StepsBorder
import Views.CountrySelect as CountrySelect
import Views.Format as Format
import Views.Icon as Icon
import Views.Link as Link
import Views.RangeSlider as RangeSlider
import Views.Transport as TransportView


type alias Config msg modal =
    { db : Db
    , addMaterialModal : Maybe Inputs.MaterialInput -> Autocomplete Material -> modal
    , current : Step
    , daysOfWear : Duration
    , useNbCycles : Int
    , deleteMaterial : Material -> msg
    , index : Int
    , inputs : Inputs
    , next : Maybe Step
    , selectedImpact : Definition
    , setModal : modal -> msg
    , showAdvancedFields : Bool
    , toggleFading : Bool -> msg
    , toggleStep : Label -> msg
    , updateAirTransportRatio : Maybe Split -> msg
    , updateCountry : Label -> Country.Code -> msg
    , updateDyeingMedium : DyeingMedium -> msg
    , updateFabricProcess : Fabric -> msg
    , updateMakingComplexity : MakingComplexity -> msg
    , updateMakingDeadStock : Maybe Split -> msg
    , updateMakingWaste : Maybe Split -> msg
    , updateMaterial : MaterialQuery -> MaterialQuery -> msg
    , updateMaterialSpinning : Material -> Spinning -> msg
    , updatePrinting : Maybe Printing -> msg
    , updateSurfaceMass : Maybe Unit.SurfaceMass -> msg
    , updateYarnSize : Maybe Unit.YarnSize -> msg
    }


type alias ViewWithTransport msg =
    { step : Html msg, transport : Html msg }


countryField : Config msg modal -> Html msg
countryField cfg =
    div []
        [ if cfg.current.editable then
            CountrySelect.view
                { attributes =
                    [ class "form-select"
                    , disabled (not cfg.current.enabled)
                    , onInput (Country.codeFromString >> cfg.updateCountry cfg.current.label)
                    ]
                , countries = cfg.db.countries
                , onSelect = cfg.updateCountry cfg.current.label
                , scope = Scope.Textile
                , selectedCountry = cfg.current.country.code
                }

          else
            div [ class "fs-6 text-muted d-flex align-items-center gap-2 " ]
                [ span
                    [ class "cursor-help"
                    , title "Le pays n'est pas modifiable à cette étape"
                    ]
                    [ Icon.lock ]
                , text cfg.current.country.name
                ]
        ]


airTransportRatioField : Config msg modal -> Html msg
airTransportRatioField { current, updateAirTransportRatio } =
    span [ title "Part de transport aérien pour le transport entre la confection et l'entrepôt en France." ]
        [ RangeSlider.percent
            { id = "airTransportRatio"
            , update = updateAirTransportRatio
            , value = current.airTransportRatio
            , toString = Step.airTransportRatioToString
            , disabled = Step.airTransportDisabled current
            , min = 0
            , max = 100
            }
        ]


dyeingMediumField : Config msg modal -> Html msg
dyeingMediumField { inputs, updateDyeingMedium } =
    div [ class "d-flex justify-content-between align-items-center fs-7" ]
        [ label [ class "text-truncate w-25", for "dyeing-medium", title "Teinture sur" ]
            [ text "Teinture sur" ]
        , [ DyeingMedium.Yarn, DyeingMedium.Fabric, DyeingMedium.Article ]
            |> List.map
                (\medium ->
                    option
                        [ value <| DyeingMedium.toString medium
                        , selected <| inputs.dyeingMedium == Just medium || inputs.product.dyeing.defaultMedium == medium
                        ]
                        [ text <| DyeingMedium.toLabel medium ]
                )
            |> select
                [ id "dyeing-medium"
                , class "form-select form-select-sm w-75"
                , onInput
                    (DyeingMedium.fromString
                        >> Result.withDefault inputs.product.dyeing.defaultMedium
                        >> updateDyeingMedium
                    )
                ]
        ]


spinningProcessField : Config msg modal -> Html msg
spinningProcessField { inputs, updateMaterialSpinning } =
    li [ class "list-group-item d-flex align-items-center gap-2" ]
        [ inputs.materials
            |> List.map
                (\{ material, spinning } ->
                    div [ class "d-flex justify-content-between align-items-center fs-7" ]
                        [ label
                            [ for <| "spinning-for-" ++ Material.idToString material.id
                            , class "text-truncate w-25"
                            ]
                            [ text material.shortName ]
                        , case Spinning.getAvailableProcesses material.origin of
                            [ spinningProcess ] ->
                                span [ class " w-75" ]
                                    [ text <| Spinning.toLabel spinningProcess ]

                            availableSpinningProcesses ->
                                availableSpinningProcesses
                                    |> List.map
                                        (\spinningProcess ->
                                            option
                                                [ value <| Spinning.toString spinningProcess
                                                , selected <| Just spinningProcess == spinning
                                                ]
                                                [ text <| Spinning.toLabel spinningProcess
                                                ]
                                        )
                                    |> select
                                        [ class "form-select form-select-sm w-75"
                                        , id <| "spinning-for-" ++ Material.idToString material.id
                                        , onInput
                                            (Spinning.fromString
                                                >> Result.withDefault (Spinning.getDefault material.origin)
                                                >> updateMaterialSpinning material
                                            )
                                        ]
                        ]
                )
            |> div [ class "d-flex flex-column gap-1 w-100" ]
        ]


fabricProcessField : Config msg modal -> Html msg
fabricProcessField { inputs, updateFabricProcess } =
    li [ class "list-group-item d-flex align-items-center gap-2" ]
        [ label [ class "text-nowrap w-25", for "fabric-process" ] [ text "Procédé" ]
        , Fabric.fabricProcesses
            |> List.map
                (\fabricProcess ->
                    option
                        [ value <| Fabric.toString fabricProcess
                        , selected <|
                            case inputs.fabricProcess of
                                Just fabric ->
                                    fabricProcess == fabric

                                Nothing ->
                                    fabricProcess == inputs.product.fabric
                        ]
                        [ text <| Fabric.toLabel fabricProcess ]
                )
            |> select
                [ id "fabric-process"
                , class "form-select form-select-sm w-75"
                , onInput
                    (Fabric.fromString
                        >> Result.withDefault Fabric.default
                        >> updateFabricProcess
                    )
                ]
        ]


printingFields : Config msg modal -> Html msg
printingFields { inputs, updatePrinting } =
    div [ class "d-flex justify-content-between align-items-center fs-7" ]
        [ label [ class "text-truncate w-25", for "ennobling-printing", title "Impression" ]
            [ text "Impression" ]
        , div [ class "d-flex justify-content-between align-items-center gap-1 w-75" ]
            [ [ Printing.Pigment, Printing.Substantive ]
                |> List.map
                    (\kind ->
                        option
                            [ value (Printing.toString kind)
                            , selected <| Maybe.map .kind inputs.printing == Just kind
                            ]
                            [ text <| Printing.kindLabel kind ]
                    )
                |> (::) (option [ selected <| inputs.printing == Nothing ] [ text "Aucune" ])
                |> select
                    [ id "ennobling-printing"
                    , class "form-select form-select-sm"
                    , style "flex" "2"
                    , onInput
                        (\str ->
                            updatePrinting
                                (case Printing.fromString str of
                                    Ok kind ->
                                        case inputs.printing of
                                            Just printing ->
                                                Just { printing | kind = kind }

                                            Nothing ->
                                                Just { kind = kind, ratio = Printing.defaultRatio }

                                    Err _ ->
                                        -- Note: we've most likely received the "Aucune" string value from
                                        -- when the user picked this choice, so it's fair to reset any
                                        -- previously selected printing process.
                                        Nothing
                                )
                        )
                    ]
            , case inputs.printing of
                Just { ratio } ->
                    [ 100, 50, 20, 5, 1 ]
                        |> List.map
                            (\percent ->
                                option
                                    [ value (String.fromFloat percent)
                                    , selected <| Ok ratio == Split.fromPercent percent
                                    ]
                                    [ text <| String.fromFloat percent ++ "%" ]
                            )
                        |> select
                            [ class "form-select form-select-sm"
                            , style "flex" "1"
                            , disabled <| inputs.printing == Nothing
                            , onInput
                                (\str ->
                                    case String.toFloat str of
                                        Just percent ->
                                            inputs.printing
                                                |> Maybe.map
                                                    (\p ->
                                                        { p
                                                            | ratio =
                                                                Split.fromPercent percent
                                                                    |> Result.toMaybe
                                                                    |> Maybe.withDefault Split.zero
                                                        }
                                                    )
                                                |> updatePrinting

                                        Nothing ->
                                            updatePrinting Nothing
                                )
                            ]

                Nothing ->
                    text ""
            ]
        ]


fadingField : Config msg modal -> Html msg
fadingField { inputs, toggleFading } =
    label
        [ class "form-check form-switch form-check-label fs-7 pt-1 text-truncate"
        , title "Délavage"
        ]
        [ input
            [ type_ "checkbox"
            , class "form-check-input no-outline"
            , inputs.fading |> Maybe.withDefault False |> checked
            , onCheck toggleFading
            ]
            []
        , if inputs.fading == Just True then
            text "Délavage activé"

          else
            text "Délavage désactivé"
        ]


makingComplexityField : Config msg modal -> Html msg
makingComplexityField ({ inputs, updateMakingComplexity } as config) =
    let
        makingComplexity =
            inputs.fabricProcess
                |> Fabric.getMakingComplexity inputs.product.making.complexity inputs.makingComplexity
    in
    li [ class "list-group-item d-flex align-items-center gap-2" ]
        [ label [ class "text-nowrap w-25", for "making-complexity" ] [ text "Complexité" ]
        , inlineDocumentationLink config Gitbook.TextileMakingComplexity
        , if inputs |> Inputs.isFabricOfType Fabric.KnittingIntegral then
            text "Non applicable"

          else
            [ MakingComplexity.VeryHigh
            , MakingComplexity.High
            , MakingComplexity.Medium
            , MakingComplexity.Low
            , MakingComplexity.VeryLow
            ]
                |> List.map
                    (\complexity ->
                        option
                            [ value <| MakingComplexity.toString complexity
                            , selected <| complexity == makingComplexity
                            ]
                            [ text <| MakingComplexity.toLabel complexity ]
                    )
                |> select
                    [ id "making-complexity"
                    , class "form-select form-select-sm w-75"
                    , disabled False
                    , onInput
                        (MakingComplexity.fromString
                            >> Result.withDefault inputs.product.making.complexity
                            >> updateMakingComplexity
                        )
                    ]
        ]


makingWasteField : Config msg modal -> Html msg
makingWasteField { current, inputs, updateMakingWaste } =
    span [ title "Taux moyen de pertes en confection" ]
        [ RangeSlider.percent
            { id = "makingWaste"
            , update = updateMakingWaste
            , value =
                inputs.fabricProcess
                    |> Fabric.getMakingWaste inputs.product.making.pcrWaste inputs.makingWaste
            , toString = Step.makingWasteToString
            , disabled = not current.enabled
            , min = Env.minMakingWasteRatio |> Split.toPercent |> round
            , max = Env.maxMakingWasteRatio |> Split.toPercent |> round
            }
        ]


makingDeadStockField : Config msg modal -> Html msg
makingDeadStockField { current, updateMakingDeadStock, showAdvancedFields } =
    showIf showAdvancedFields <|
        span [ title "Taux moyen de stocks dormants (vêtements non vendus + produits semi-finis non utilisés) sur l’ensemble de la chaîne de valeur" ]
            [ RangeSlider.percent
                { id = "makingDeadStock"
                , update = updateMakingDeadStock
                , value = Maybe.withDefault Env.defaultDeadStock current.makingDeadStock
                , toString = Step.makingDeadStockToString
                , disabled = False
                , min = Env.minMakingDeadStockRatio |> Split.toPercent |> round
                , max = Env.maxMakingDeadStockRatio |> Split.toPercent |> round
                }
            ]


surfaceMassField : Config msg modal -> Html msg
surfaceMassField { current, updateSurfaceMass, inputs } =
    div
        [ class "mt-2"
        , title "Le grammage de l'étoffe, exprimé en g/m², représente sa masse surfacique."
        ]
        [ RangeSlider.surfaceMass
            { id = "surface-density"
            , update = updateSurfaceMass
            , value = current.surfaceMass |> Maybe.withDefault inputs.product.surfaceMass
            , toString = Step.surfaceMassToString

            -- Note: hide for knitted products as surface mass doesn't have any impact on them
            , disabled = not current.enabled
            }
        ]


yarnSizeField : Config msg modal -> Html msg
yarnSizeField { current, updateYarnSize, inputs } =
    span [ title "Le titrage indique la grosseur d’un fil textile" ]
        [ RangeSlider.yarnSize
            { id = "yarnSize"
            , update = updateYarnSize
            , value = current.yarnSize |> Maybe.withDefault inputs.product.yarnSize
            , toString = Step.yarnSizeToString
            , disabled = not current.enabled
            }
        ]


inlineDocumentationLink : Config msg modal -> Gitbook.Path -> Html msg
inlineDocumentationLink _ path =
    Button.smallPillLink
        [ href (Gitbook.publicUrlFromPath path)
        , target "_blank"
        ]
        [ Icon.question ]


stepActions : Config msg modal -> Label -> Html msg
stepActions { current, showAdvancedFields, toggleStep } label =
    let
        allowDisablingStep =
            showAdvancedFields
                -- Regulatory mode only allow disabling Spinning, Fabric and Ennobling steps
                || List.member current.label
                    [ Label.Material
                    , Label.Spinning
                    , Label.Fabric
                    , Label.Ennobling
                    ]
    in
    div [ class "StepActions ms-2" ]
        [ div [ class "btn-group" ]
            [ Button.docsPillLink
                [ class "btn btn-secondary py-1 rounded"
                , href (Gitbook.publicUrlFromPath (Label.toGitbookPath label))
                , title "Documentation"
                , target "_blank"
                ]
                [ Icon.question ]
            , showIf allowDisablingStep <|
                input
                    [ type_ "checkbox"
                    , class "form-check-input ms-1 no-outline"
                    , attribute "role" "switch"
                    , checked current.enabled
                    , onCheck (always (toggleStep current.label))
                    , title
                        (if current.enabled then
                            "Étape activée, cliquez pour la désactiver"

                         else
                            "Étape desactivée, cliquez pour la réactiver"
                        )
                    ]
                    []
            ]
        ]


viewStepImpacts : Definition -> Step -> Html msg
viewStepImpacts selectedImpact { impacts, complementsImpacts } =
    showIf (Quantity.greaterThanZero (Impact.getImpact selectedImpact.trigram impacts)) <|
        let
            stepComplementsImpact =
                complementsImpacts
                    |> Impact.getTotalComplementsImpacts

            totalImpacts =
                impacts
                    |> Impact.applyComplements stepComplementsImpact
        in
        div []
            [ span [ class "flex-fill" ]
                [ totalImpacts
                    |> Format.formatImpact selectedImpact
                ]
            ]


viewMaterials : Config msg modal -> Html msg
viewMaterials config =
    ul [ class "CardList list-group list-group-flush" ]
        ((config.inputs.materials
            |> List.map
                (\materialInput ->
                    let
                        nextCountry =
                            config.next
                                |> Maybe.withDefault config.current
                                |> .country

                        transport =
                            materialInput
                                |> Step.computeMaterialTransportAndImpact config.db nextCountry config.current.outputMass
                    in
                    li [ class "ElementFormWrapper list-group-item" ]
                        (List.concat
                            [ materialInput
                                |> createElementSelectorConfig config
                                |> BaseElement.view
                            , if config.selectedImpact.trigram == Definition.Ecs then
                                [ materialInput
                                    |> viewMaterialComplements config.inputs.mass
                                ]

                              else
                                []
                            , [ span [ class "text-muted d-flex fs-7 gap-3 justify-content-left ElementTransportDistances" ]
                                    (transport
                                        |> TransportView.viewDetails
                                            { fullWidth = False
                                            , hideNoLength = True
                                            , onlyIcons = False
                                            , airTransportLabel = Nothing
                                            , seaTransportLabel = Nothing
                                            , roadTransportLabel = Nothing
                                            }
                                    )
                              , span
                                    [ class "text-black-50 text-end ElementTransportImpact fs-8"
                                    , title "Impact du transport pour cette matière"
                                    ]
                                    [ text "(+ "
                                    , Format.formatImpact config.selectedImpact transport.impacts
                                    , text ")"
                                    ]
                              ]
                            ]
                        )
                )
         )
            ++ [ let
                    length =
                        List.length config.inputs.materials

                    excluded =
                        config.inputs.materials
                            |> List.map .material

                    availableMaterials =
                        config.db.textile.materials
                            |> List.filter (\element -> not (List.member element excluded))

                    totalShares =
                        config.inputs.materials
                            |> List.map (.share >> Split.toFloat >> clamp 0 1)
                            |> List.sum

                    valid =
                        round (totalShares * 100) == 100
                 in
                 li
                    [ class "input-group AddElementFormWrapper ps-3" ]
                    [ span
                        [ class "SharesTotal ext-end"
                        , class "d-flex justify-content-between align-items-center gap-1"
                        , classList
                            [ ( "text-success feedback-valid", valid )
                            , ( "text-danger feedback-invalid", not valid )
                            ]
                        ]
                        [ if valid then
                            Icon.check

                          else
                            Icon.warning
                        , round (totalShares * 100) |> String.fromInt |> text
                        , text "%"
                        ]
                    , button
                        [ class "AddElementButton btn btn-outline-primary flex-fill"
                        , class "d-flex justify-content-center align-items-center gap-1 no-outline"
                        , id "add-new-element"
                        , availableMaterials
                            |> List.sortBy .shortName
                            |> AutocompleteSelector.init .shortName
                            |> config.addMaterialModal Nothing
                            |> config.setModal
                            |> onClick
                        , disabled <| length >= Env.maxMaterials
                        ]
                        [ Icon.plus
                        , if length >= Env.maxMaterials then
                            text "Nombre maximal de matières atteint"

                          else
                            text "Ajouter une matière"
                        ]
                    ]
               ]
        )


viewMaterialComplements : Mass -> Inputs.MaterialInput -> Html msg
viewMaterialComplements finalProductMass materialInput =
    let
        materialComplement =
            Inputs.getMaterialMicrofibersComplement finalProductMass materialInput

        materialComplementsImpacts =
            { noComplementsImpacts | microfibers = materialComplement }
    in
    ComplementsDetails.view
        { complementsImpacts = materialComplementsImpacts
        , label = "Compléments"
        }
        [ div [ class "ElementComplement", title "Microfibres" ]
            [ span [ class "ComplementName d-flex align-items-center text-nowrap text-muted" ]
                [ text "Microfibres"
                , Button.smallPillLink
                    [ href (Gitbook.publicUrlFromPath Gitbook.TextileComplementMicrofibers)
                    , target "_blank"
                    ]
                    [ Icon.question ]
                ]
            , span [ class "ComplementRange" ] []
            , div [ class "ComplementValue d-flex" ] []
            , div [ class "ComplementImpact text-black-50 text-muted text-end" ]
                [ text "("
                , Format.complement materialComplement
                , text ")"
                ]
            ]
        ]


createElementSelectorConfig : Config msg modal -> Inputs.MaterialInput -> BaseElement.Config Material Split msg
createElementSelectorConfig cfg materialInput =
    let
        materialQuery : MaterialQuery
        materialQuery =
            { id = materialInput.material.id
            , share = materialInput.share
            , spinning = materialInput.spinning
            , country = materialInput.country |> Maybe.map .code
            }

        baseElement =
            { element = materialInput.material
            , quantity = materialInput.share
            , country = materialInput.country
            }

        excluded =
            cfg.inputs.materials
                |> List.map .material

        impacts =
            cfg.current
                |> stepMaterialImpacts cfg.db materialInput.material
                |> Impact.mapImpacts (\_ -> Quantity.multiplyBy (Split.toFloat materialInput.share))
    in
    { allowEmptyList = False
    , baseElement = baseElement
    , db =
        { elements = cfg.db.textile.materials
        , countries =
            cfg.db.countries
                |> Scope.only Scope.Textile
                |> List.sortBy .name
        , definitions = cfg.db.definitions
        }
    , defaultCountry = materialInput.material.geographicOrigin
    , delete = cfg.deleteMaterial
    , excluded = excluded
    , impact = impacts
    , selectedImpact = cfg.selectedImpact
    , selectElement = \_ autocompleteState -> cfg.setModal (cfg.addMaterialModal (Just materialInput) autocompleteState)
    , quantityView =
        \{ quantity, onChange } ->
            SplitInput.view
                { disabled = False
                , share = quantity
                , onChange = onChange
                }
    , toId = .id >> Material.idToString
    , toString = .shortName
    , toTooltip = .materialProcess >> .name
    , update =
        \_ newElement ->
            cfg.updateMaterial
                materialQuery
                { materialQuery
                    | id = newElement.element.id
                    , share = newElement.quantity
                    , country = newElement.country |> Maybe.map .code
                }
    }


viewTransport : Config msg modal -> Html msg
viewTransport ({ selectedImpact, current, inputs } as config) =
    div []
        [ span []
            [ text "Masse\u{00A0}: "
            , current |> Step.getTransportedMass inputs |> Format.kg
            ]
        , showIf (Transport.totalKm current.transport > 0) <|
            div [ class "d-flex justify-content-between gap-3 align-items-center" ]
                [ div [ class "d-flex justify-content-between gap-3 flex-column flex-md-row" ]
                    (current.transport
                        |> TransportView.viewDetails
                            { fullWidth = False
                            , hideNoLength = True
                            , onlyIcons = False
                            , airTransportLabel = Nothing
                            , seaTransportLabel = Nothing
                            , roadTransportLabel = Nothing
                            }
                    )
                , span []
                    [ current.transport.impacts
                        |> Format.formatImpact selectedImpact
                    , inlineDocumentationLink config Gitbook.TextileTransport
                    ]
                ]
        ]


viewProcessInfo : Maybe String -> Html msg
viewProcessInfo processName =
    case processName of
        Just name ->
            li
                [ class "list-group-item text-truncate"
                , title name
                , style "cursor" "help"
                ]
                [ text name ]

        Nothing ->
            text ""


daysOfWearInfo : Config msg modal -> Html msg
daysOfWearInfo { daysOfWear, useNbCycles } =
    small
        [ class "d-flex align-items-center fs-7 cursor-help"
        , title "Nombre dépendant de la catégorie de vêtement et du coefficient de durabilité"
        ]
        [ span [ class "pe-1 text-muted" ] [ Icon.info ]
        , Format.days daysOfWear
        , text "\u{00A0}portés, "
        , text <| String.fromInt useNbCycles
        , text <|
            " cycle"
                ++ (if useNbCycles > 1 then
                        "s"

                    else
                        ""
                   )
                ++ " d'entretien"
        ]


ennoblingGenericFields : Config msg modal -> Html msg
ennoblingGenericFields config =
    -- Note: this fieldset is rendered in both simple and detailed step views
    div [ class "d-flex flex-column gap-1" ]
        [ showIf config.showAdvancedFields <|
            dyeingMediumField config
        , printingFields config
        ]


surfaceInfoView : Inputs -> Step -> Html msg
surfaceInfoView inputs current =
    let
        surfaceInfo =
            if current.label == Label.Fabric then
                Just ( "sortante", Step.getOutputSurface inputs current )

            else if current.label == Label.Ennobling then
                Just ( "entrante", Step.getInputSurface inputs current )

            else
                Nothing
    in
    case surfaceInfo of
        Just ( dir, surface ) ->
            li [ class "list-group-item text-muted d-flex justify-content-center gap-2" ]
                [ span [] [ text <| "Surface étoffe (" ++ dir ++ ")\u{00A0}:" ]
                , span [] [ Format.squareMeters surface ]
                ]

        Nothing ->
            text ""


ennoblingToxicityView : Db -> Config msg modal -> Step -> Html msg
ennoblingToxicityView db ({ selectedImpact, inputs } as config) current =
    showIf (current.label == Label.Ennobling) <|
        let
            bleachingToxicity =
                current.outputMass
                    |> Formula.bleachingImpacts current.impacts
                        { bleachingProcess = db.textile.wellKnown.bleaching
                        , aquaticPollutionScenario = current.country.aquaticPollutionScenario
                        }

            dyeingToxicity =
                inputs.materials
                    |> List.map
                        (\{ material, share } ->
                            Formula.materialDyeingToxicityImpacts current.impacts
                                { dyeingToxicityProcess =
                                    if Origin.isSynthetic material.origin then
                                        db.textile.wellKnown.dyeingSynthetic

                                    else
                                        db.textile.wellKnown.dyeingCellulosic
                                , aquaticPollutionScenario = current.country.aquaticPollutionScenario
                                }
                                current.outputMass
                                share
                        )
                    |> Impact.sumImpacts

            printingToxicity =
                case current.printing of
                    Just { kind, ratio } ->
                        let
                            { printingToxicityProcess } =
                                WellKnown.getPrintingProcess kind db.textile.wellKnown
                        in
                        current.outputMass
                            |> Formula.materialPrintingToxicityImpacts
                                current.impacts
                                { printingToxicityProcess = printingToxicityProcess
                                , aquaticPollutionScenario = current.country.aquaticPollutionScenario
                                }
                                ratio

                    Nothing ->
                        Impact.empty

            toxicity =
                Impact.sumImpacts [ bleachingToxicity, dyeingToxicity, printingToxicity ]
        in
        li [ class "list-group-item text-muted d-flex justify-content-center gap-2" ]
            [ span [] [ text <| "Dont inventaires enrichis\u{00A0}:" ]
            , span [ class "text-end ImpactDisplay text-black-50 fs-7" ]
                [ text "(+\u{00A0}"
                , toxicity
                    |> Format.formatImpact selectedImpact
                , text ")"
                , inlineDocumentationLink config Gitbook.TextileEnnoblingToxicity
                ]
            ]


pickingView : Maybe Unit.PickPerMeter -> Html msg
pickingView maybePicking =
    case maybePicking of
        Just picking ->
            li [ class "list-group-item text-muted d-flex justify-content-center gap-2" ]
                [ text "Duitage\u{00A0}:\u{00A0}"
                , picking
                    |> Unit.pickPerMeterToFloat
                    |> Format.formatRichFloat 0 "duites.m"
                ]

        Nothing ->
            text ""


threadDensityView : Maybe Unit.ThreadDensity -> Html msg
threadDensityView threadDensity =
    case threadDensity of
        Just density ->
            let
                value =
                    Unit.threadDensityToFloat density
            in
            li [ class "list-group-item text-muted" ]
                [ span [ class "d-flex justify-content-center gap-2" ]
                    [ text "Densité de fils (approx.)\u{00A0}:\u{00A0}"
                    , value
                        |> Format.formatRichFloat 0 "fils/cm"
                    ]
                , if round value < Unit.threadDensityToInt Unit.threadDensityLow then
                    text "⚠️ la densité de fils semble très faible"

                  else if round value > Unit.threadDensityToInt Unit.threadDensityHigh then
                    text "⚠️ la densité de fils semble très élevée"

                  else
                    text ""
                ]

        Nothing ->
            text ""


deadstockView : Config msg modal -> Mass -> Html msg
deadstockView config deadstock =
    showIf (config.current.label == Label.Making) <|
        li [ class "list-group-item text-muted d-flex justify-content-center gap-2" ]
            (if deadstock /= Quantity.zero then
                [ text "Dont stocks dormants\u{00A0}:\u{00A0}"
                , Format.kgToString deadstock |> text
                , inlineDocumentationLink config Gitbook.TextileMakingDeadStock
                ]

             else
                [ text "Aucun stock dormant." ]
            )


makingWasteView : Config msg modal -> Mass -> Html msg
makingWasteView config waste =
    showIf (config.current.label == Label.Making) <|
        li [ class "list-group-item text-muted d-flex justify-content-center gap-2" ]
            (if waste /= Quantity.zero then
                [ text "Pertes\u{00A0}:\u{00A0}"
                , Format.kgToString waste |> text
                , inlineDocumentationLink config Gitbook.TextileMakingMakingWaste
                ]

             else
                [ text "Aucune perte en confection." ]
            )


showIf : Bool -> Html msg -> Html msg
showIf flag html =
    if flag then
        html

    else
        text ""


stepView : Config msg modal -> Html msg -> Html msg
stepView ({ current } as config) html =
    div [ class "Step card shadow-sm" ]
        [ div
            [ class "StepHeader card-header"
            , StepsBorder.style <| Label.toColor current.label
            , id <| Label.toId current.label
            ]
            [ div [ class "row d-flex align-items-center" ]
                [ div [ class "col-9 col-sm-6" ]
                    [ div
                        [ class "d-flex align-items-center gap-2 text-dark"
                        , classList [ ( "text-secondary", not current.enabled ) ]
                        ]
                        [ h2 [ class "h5 mb-0" ]
                            [ current.label
                                |> Label.toName
                                |> text
                            , showIf (current.label == Label.Material) <|
                                Link.smallPillExternal
                                    [ Route.href (Route.Explore Scope.Textile (Dataset.TextileMaterials Nothing))
                                    , title "Explorer"
                                    , attribute "aria-label" "Explorer"
                                    ]
                                    [ Icon.search ]
                            ]
                        ]
                    ]
                , div [ class "col-3 col-sm-6 d-flex text-end justify-content-end" ]
                    [ div [ class "d-none d-sm-block text-center" ]
                        [ viewStepImpacts config.selectedImpact current
                        ]
                    , stepActions config current.label
                    ]
                ]
            ]
        , html
        ]


regulatoryStepView : Config msg modal -> Html msg
regulatoryStepView ({ current } as config) =
    div
        [ class "StepBody card-body row align-items-center" ]
        [ div [ class "col-lg-7" ]
            [ countryField config
            , case current.label of
                Label.Ennobling ->
                    div [ class "mt-2" ]
                        [ ennoblingGenericFields config
                        ]

                Label.Making ->
                    div [ class "mt-2" ]
                        [ airTransportRatioField config
                        , fadingField config
                        ]

                Label.Use ->
                    div [ class "mt-2" ]
                        [ daysOfWearInfo config
                        ]

                _ ->
                    text ""
            ]
        ]


advancedStepView : Config msg modal -> Html msg
advancedStepView ({ db, inputs, selectedImpact, current } as config) =
    let
        infoListElement =
            ul
                [ class "StepBody list-group list-group-flush fs-7 border-bottom-0"
                , classList [ ( "disabled", not current.enabled ) ]
                ]
    in
    div [ class "card-group" ]
        [ div [ class "card border-start-0 border-top-0 border-bottom-0" ]
            [ infoListElement
                [ li [ class "list-group-item" ] [ countryField config ]
                , viewProcessInfo <| Maybe.map ((++) "Elec : ") current.processInfo.countryElec
                , viewProcessInfo <| Maybe.map ((++) "Chaleur : ") current.processInfo.countryHeat
                , viewProcessInfo current.processInfo.distribution
                , viewProcessInfo current.processInfo.useIroning
                , viewProcessInfo current.processInfo.useNonIroning
                , viewProcessInfo current.processInfo.passengerCar
                , viewProcessInfo current.processInfo.endOfLife
                , showIf (current.label == Label.Spinning) <| spinningProcessField config
                , showIf (current.label == Label.Fabric) <| fabricProcessField config
                , showIf (current.label == Label.Making) <| makingComplexityField config
                , showIf (inputs.fading == Just True) <| viewProcessInfo current.processInfo.fading
                ]
            , ul
                [ class "StepBody p-0 list-group list-group-flush border-bottom-0"
                , classList [ ( "disabled", not current.enabled ) ]
                ]
                (List.map
                    (\line -> li [ class "list-group-item fs-7" ] [ line ])
                    (case current.label of
                        Label.Spinning ->
                            [ yarnSizeField config
                            ]

                        Label.Fabric ->
                            [ surfaceMassField config ]

                        Label.Ennobling ->
                            [ div [ class "mb-2" ]
                                [ text "Pré-traitement\u{00A0}: non applicable" ]
                            , ennoblingGenericFields config
                            , div [ class "mt-2" ]
                                [ text "Finition\u{00A0}: apprêt chimique" ]
                            ]

                        Label.Making ->
                            List.filterMap identity
                                [ Just <| makingWasteField config
                                , Just <| makingDeadStockField config
                                , Just <| airTransportRatioField config
                                , Just (fadingField config)
                                ]

                        Label.Use ->
                            [ daysOfWearInfo config
                            ]

                        _ ->
                            []
                    )
                )
            ]
        , div [ class "card border-end-0 border-top-0 border-bottom-0 text-center mb-0" ]
            [ ul
                [ class "StepBody list-group list-group-flush fs-7"
                , classList [ ( "disabled", not current.enabled ) ]
                ]
                [ showIf (Energy.inKilojoules current.heat > 0 || Energy.inKilowattHours current.kwh > 0) <|
                    li [ class "list-group-item text-muted d-flex flex-wrap justify-content-around" ]
                        [ span [ class "d-flex align-items-center" ]
                            [ span [ class "me-1" ] [ text "Chaleur" ]
                            , Format.megajoules current.heat
                            , inlineDocumentationLink config Gitbook.TextileHeat
                            ]
                        , span [ class "d-flex align-items-center" ]
                            [ span [ class "me-1" ] [ text "Électricité" ]
                            , Format.kilowattHours current.kwh
                            , inlineDocumentationLink config Gitbook.TextileElectricity
                            ]
                        ]
                , surfaceInfoView inputs current
                , ennoblingToxicityView db config current
                , pickingView current.picking
                , threadDensityView current.threadDensity
                , makingWasteView config current.waste
                , deadstockView config current.deadstock
                , showIf (current.label == Label.EndOfLife) <|
                    li [ class "list-group-item text-muted" ]
                        [ div [ class "d-flex justify-content-between" ]
                            [ text "Fin de vie"
                            , Format.formatImpact selectedImpact current.impacts
                            ]
                        , showIf (selectedImpact.trigram == Definition.Ecs) <|
                            div [ class "text-start mt-2" ]
                                [ span [ class "fw-bold" ] [ text "Complément" ]
                                , div [ class "d-flex justify-content-between" ]
                                    [ text "-\u{00A0}Export hors-Europe"
                                    , Format.complement current.complementsImpacts.outOfEuropeEOL
                                    ]
                                , div [ class "d-flex justify-content-between" ]
                                    [ span [ class "me-2 text-truncate" ] [ text "-\u{00A0}Probabilité de fin de vie hors-Europe" ]
                                    , span [ class "text-nowrap" ]
                                        [ inputs.materials
                                            |> Inputs.getOutOfEuropeEOLProbability
                                            |> Format.splitAsPercentage 2
                                        , inlineDocumentationLink config Gitbook.TextileEndOfLifeOutOfEuropeComplement
                                        ]
                                    ]
                                ]
                        ]
                ]
            ]
        ]


view : Config msg modal -> ViewWithTransport msg
view config =
    { transport = viewTransport config
    , step =
        stepView config
            (if config.current.label == Label.Material then
                viewMaterials config

             else if config.showAdvancedFields then
                advancedStepView config

             else
                regulatoryStepView config
            )
    }
